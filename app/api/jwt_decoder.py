import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

superadmin = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwODU3ODY1NDksInJvbGUiOiJzdXBlcmFkbWluIiwidWlkIjozM30.uz_2FO8CX520sNcv5-EILixUQRqS5zuZrWb9lUyw6uE"
admin = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwODU3ODY3MjUsInJvbGUiOiJhZG1pbiIsInVpZCI6MTJ9.N5MW76x-ko3HbeFZioYzdyRzC983c3LUejx_kpCrty4"
user = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwODU3ODY3MDIsInJvbGUiOiJ1c2VyIiwidWlkIjoyN30.w7cLH7CK-JUhTLwRUSknoTLYwGFERH1e-brrqH9QFEY"

def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "test", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
current_user = decode_token(user)