import re
import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import SECRET


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
EXEMPT_PATHS = [r"/content/image/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}"]


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request.state.role = None
        request.state.uid = None

        if request.url.path.startswith(("/content/docs", "/content/redoc", "/content/openapi.json")):
            return await call_next(request)

        if self.is_exempt_path(request.url.path):
            return await call_next(request)

        token = request.headers.get("authorization")

        try:
            if "Bearer" in token:
                token = token.split(" ")[1]
            request.state.role = self.decode_token(token)["role"]
            request.state.uid = self.decode_token(token)["uid"]
            jwt.decode(token, SECRET, algorithms=["HS256"])
            return await call_next(request)

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token has expired"})

        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        except AttributeError and TypeError:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        except Exception:
            return JSONResponse(status_code=500, content={"detail": "Others errors"})

    def decode_token(self, token: str) -> bool:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload

    def is_exempt_path(self, path: str):
        for exempt_path in EXEMPT_PATHS:
            if re.fullmatch(exempt_path, path):
                return True
        return False
