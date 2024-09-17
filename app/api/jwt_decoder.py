import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "test", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
current_user = decode_token(user)
