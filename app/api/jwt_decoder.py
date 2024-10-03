import jwt
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("authorization")
        if not token or not self.validate_token(token.split(" ")[1]):
            raise HTTPException(status_code=401, detail="Unauthorized")
        token = token.split(" ")[1]
        request.state.role = self.decode_token(token)["role"]
        response = await call_next(request)
        return response

    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(token, "test", algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    def decode_token(self, token: str) -> bool:
        payload = jwt.decode(token, "test", algorithms=["HS256"])
        return payload
    
