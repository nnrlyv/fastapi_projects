import logging
import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from src.config import config
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer

passwd_context = CryptContext( #hashing algorithm
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_uid: uuid.UUID, user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        "user_uid": str(user_uid),
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes = 60)),
        'refresh': refresh,
        'jti': str(uuid.uuid4())  # <--- вот это добавь
    }

    token = jwt.encode(
        payload = payload,
        key = config.JWT_SECRET,
        algorithm = config.JWT_ALGORITHM,

    )

    return token

def decode_token(token:str ) -> dict:
    try:
        token_data = jwt.decode(
            jwt = token,
            key=config.JWT_SECRET,
            algorithms = [config.JWT_ALGORITHM]
        )
        print("✅ Token decoded:", token_data)  # 👈 добавь эту строку
        return token_data
    except jwt.PyJWTError as jwte:
        print("❌ JWT decode error:", jwte)  # 👈 и эту
        logging.exception(jwte)
        return None

        """"" return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None

    except Exception as e:
        logging.exception(e)
        return None"""


salt = "email-verification"
serializer = URLSafeTimedSerializer(
    secret_key = config.JWT_SECRET)

def create_url_safe_token(data:dict)-> str:

    return serializer.dumps(data, salt=salt)

def decode_url_safe_token(token:str,max_age=3600)-> dict:
    try:
        # Deserialize the token and check if it's expired
        data = serializer.loads(token, salt=salt, max_age=max_age)
        return data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")



















