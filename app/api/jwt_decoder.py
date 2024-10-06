import jwt
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Проверка на /docs или /redoc
        if request.url.path.startswith(("/content/docs", "/content/redoc", "/content/openapi.json")):
            return await call_next(request)

        token = request.headers.get("authorization")
        if token:
            token = token.split(" ")[1]
            if not self.validate_token(token):
                raise HTTPException(status_code=401, detail="Unauthorized")
            request.state.role = self.decode_token(token)["role"]
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
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
