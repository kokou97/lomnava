from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algorithm
# Expiration time
# openssl rand -hex 32 in ubuntu terminal
SECRET_KEY = "e764fa8d2f62a445c26b07372ba5737c4b2a1ab68da4f453e70a8ed36c595709"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt
