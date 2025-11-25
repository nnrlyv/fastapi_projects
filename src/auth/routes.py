from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,status
from fastapi import BackgroundTasks

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel, EmailModel, \
    PasswordResetConfirmModel, PasswordResetRequestModel
from src.auth.service import UserService
from src.auth.utils import verify_password, create_access_token, create_url_safe_token, decode_url_safe_token, \
    generate_password_hash
from src.db.main import get_session

from fastapi.exceptions import HTTPException
from src.config import config
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, UserNotFound
from src.mail import mail , create_message

from .utils import (create_url_safe_token,decode_url_safe_token)

auth_router = APIRouter()
user_service = UserService()

admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker(["user"])
REFRESH_TOKEN_EXPIRY = 2

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(admin_role_checker)):
    return user

@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email,session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)
        return JSONResponse(
            content = {"msg":"Account verified successfully!"}, status_code=status.HTTP_200_OK)

    return JSONResponse(content={"message": "Error occured during verification"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@auth_router.post("/send_mail")
async def send_mail(emails:EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the BOOKLY App!</h1>"
    subject = "Welcome to our app"

    message = create_message(recipients=emails, subject=subject,body=html)
    await mail.send_message(message)
    return {"msg":"Email sent successfully!"}


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,bg_tasks: BackgroundTasks, session:AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists =await user_service.user_exists(email,session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data,session)
    token = create_url_safe_token({"email": email })
    link = f"http://{config.DOMAIN}/auth/verify/{token}"

    html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

    message = create_message(recipients=[email], subject="Verify Your Email", body = html_message)
    bg_tasks.add_task(mail.send_message,message)
    return {"msg":"Account created! Check email for verifying account",
            "user": new_user }


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user =  await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_uid=str(user.uid),
                user_data={"email": user.email, "user_uid":str(user.uid)}
            )

            refresh_token = create_access_token(
                user_uid=str(user.uid),
                user_data={"email": user.email, "user_uid":str(user.uid)},
                refresh=True,
                expiry=timedelta(days=config.REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid":str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email": email})

    link = f"http://{config.DOMAIN}/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """

    message = create_message(recipients=[email], subject="Reset Your Password", body=html_message)
    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(token: str,passwords: PasswordResetConfirmModel,session: AsyncSession = Depends(get_session)):

    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )