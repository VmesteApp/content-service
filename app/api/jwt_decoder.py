import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/content/docs", "/content/redoc", "/content/openapi.json")):
            return await call_next(request)

        token = request.headers.get("authorization")

        try:
            if "Bearer" in token:
                token = token.split(" ")[1]
            request.state.role = self.decode_token(token)["role"]
            request.state.uid = self.decode_token(token)["uid"]
            jwt.decode(token, "test", algorithms=["HS256"])
            response = await call_next(request)
            return response

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token has expired"})

        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        except AttributeError and TypeError:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        except Exception:
            return JSONResponse(status_code=500, content={"detail": "Others errors"})

    def decode_token(self, token: str) -> bool:
        payload = jwt.decode(token, "test", algorithms=["HS256"])
        return payload
