from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException
from jwt import InvalidTokenError
from app.core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password: str):
  return pwd_context.hash(password)

def check_password_hash(plain: str, hashed: str):
  return pwd_context.verify(plain, hashed)

def create_token(payload: dict):
  exp = datetime.now() + timedelta(minutes=settings.TOKEN_LIFESPAN)
  payload.update({"exp":exp})
  token = jwt.encode(payload,settings.SECRET_KEY,settings.ALGORITHM)
  return token

def decode_token(token: str):
  credential_exception = HTTPException(status_code=401, detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    username = payload.get("username", None)
    if not username:
      raise credential_exception
  except InvalidTokenError:
    raise credential_exception
  return username

