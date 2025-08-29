from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException
from jwt import InvalidTokenError
from app.core.config import TOKEN_LIFESPAN, ALGORITHM, SECRET_KEY
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password: str):
  return pwd_context.hash(password)

def check_password_hash(plain: str, hashed: str):
  return pwd_context.verify(plain, hashed)

def create_token(payload: dict):
  exp = datetime.now() + timedelta(minutes=TOKEN_LIFESPAN)
  payload.update({"exp":exp})
  token = jwt.encode(payload,SECRET_KEY,ALGORITHM)
  return token

def decode_token(token: str):
  credential_exception = HTTPException(status_code=401, detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
  try:
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    username = payload.get("username", None)
    if not username:
      raise credential_exception
  except InvalidTokenError:
    raise credential_exception
  return username

