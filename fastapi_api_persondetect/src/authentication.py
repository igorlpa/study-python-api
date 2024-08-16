
from .enviroment import SECRET_KEY
from schema.schemas import LoginOut
import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

        
    



ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: AccessToken


def sign_jwt(secret_key: str) -> JWTToken:
    if SECRET_KEY is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Secret key is not set")

    now = time.time()
    payload = {
        "iss": "fastapi - person detector",
        "sub": 10,
        "aud": "fastapi-detector",
        "exp": now + (60 * 30),  # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    result = LoginOut(token=token)
    return result


async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, audience="fastapi-detector", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        return _token if _token.access_token.exp >= time.time() else None
    except Exception as e:
        print(e)
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")
        print('JWT credentials', credentials)
        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme. No Bearer")

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token. Not payload")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code. No credentials")


async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
    print('get_current_user ', token.access_token.sub)
    return {"token": token.access_token.sub}


def login_required(current_user: Annotated[dict[str, str], Depends(get_current_user)]):
    print('login_required')
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied!!")
    return current_user