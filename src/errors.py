from typing import Any, Callable
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI,status


class BooklyException(Exception):
    #this is base class for all bookly errors
    pass

class AccountNotVerified(Exception):
    pass

class InvalidToken(BooklyException):
    #this is for invalid or expired token
    pass

class RevokedToken(BooklyException):
    #this is for revoked token
    pass

class AccessTokenRequired(BooklyException):
    #this is for when you provided refresh token not access one
    pass

class RefreshTokenRequired(BooklyException):
    #this is when you provided access token instead of refresh one
    pass

class UserAlreadyExists(BooklyException):
    #this is when user provided email that already was used before
    pass

class InvalidCredentials(BooklyException):
    #this is when user provided wrong email or password during log in
    pass

class NoPermission(BooklyException):
    #this is when user do not have privilege to perform some actions
    pass

class BookNotFound(BooklyException):
    #this is when book not found
    pass

class TagNotFound(BooklyException):
    #Tag not found
    pass

class TagAlreadyExists(BooklyException):
    #Tag already exists
    pass

class UserNotFound(BooklyException):
    #User not found
    pass



def create_exception_handler(status_code:int, initial_detail:Any)->Callable[[Request,Exception],JSONResponse]:
    async def exception_handler(request:Request, exc:BooklyException):
        return JSONResponse(content = initial_detail, status_code=status_code)
    return exception_handler


def register_error_handlers(app:FastAPI):
    app.add_exception_handler(AccountNotVerified,
        create_exception_handler(status_code=status.HTTP_403_FORBIDDEN,
                                 initial_detail={"msg": "Account Not Verified",
                                                 "error_code": "Account_Not_Verified",
                                                 "resolution": "Please check your email for verification details"}))

    app.add_exception_handler(UserAlreadyExists,
        create_exception_handler(status_code=status.HTTP_403_FORBIDDEN,
                                 initial_detail={"msg": "User with email already exists",
                                                 "error_code": "user_exists"}))

    app.add_exception_handler(UserNotFound,
        create_exception_handler(status_code=status.HTTP_404_NOT_FOUND,
                                initial_detail={"msg": "User Not Found",
                                                "error_code": "user_not_found"}))

    app.add_exception_handler(BookNotFound,
        create_exception_handler(status_code=status.HTTP_404_NOT_FOUND,
                                initial_detail={"msg": "Book Not Found",
                                                "error_code": "book_not_found"}))

    app.add_exception_handler(InvalidCredentials,
        create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST,
                                initial_detail={"msg": "Invalid Email or Password",
                                                "error_code": "invalid_email_or_password"}))

    app.add_exception_handler(RevokedToken,
        create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED,
                                 initial_detail={"msg": "Token is invalid or has been revoked",
                                                 "resolution": "Please get new token",
                                                 "error_code": "token_revoked"}))


    app.add_exception_handler(InvalidToken,
        create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED,
                                 initial_detail={"msg": "Token is invalid or expired",
                                                 "resolution": "Please get new token",
                                                 "error_code": "invalid_token"}))



    app.add_exception_handler(AccessTokenRequired,
        create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED,
                                 initial_detail={"msg": "Please provide valid access token",
                                                 "resolution": "Please get an access token",
                                                 "error_code": "access_token_required"}))


    app.add_exception_handler(RefreshTokenRequired,
        create_exception_handler(status_code=status.HTTP_403_FORBIDDEN,
                                 initial_detail={"msg": "Please provide a valid refresh token",
                                                 "resolution": "Please get refresh token",
                                                 "error_code": "refresh_token_required"}))

    app.add_exception_handler(NoPermission,
        create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED,
                                 initial_detail={"msg": "You do not have enough permissions to perform this action",
                                                 "error_code": "insufficient_permissions"}))

    app.add_exception_handler(NoPermission,
        create_exception_handler(status_code=status.HTTP_404_NOT_FOUND,
                                initial_detail={"msg": "Tag not found",
                                                "error_code": "tag_not_found"}))


    app.add_exception_handler(TagAlreadyExists,
        create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED,
                                 initial_detail={"msg": "Tag Already exists",
                                                 "error_code": "tag_exists"}))


    app.add_exception_handler(BookNotFound,
        create_exception_handler(status_code=status.HTTP_404_NOT_FOUND,
                                 initial_detail={"msg": "Book Not Found",
                                                 "error_code": "book_not_found"}))

    @app.exception_handler(505)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



