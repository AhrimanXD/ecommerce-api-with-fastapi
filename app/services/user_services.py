from app.schemas.users import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.users import User
from fastapi import HTTPException
from app.auth.utils import hash_password, create_token,check_password_hash

def create_user(user:UserCreate, session:Session):
  existing_user = session.query(User).filter(or_(User.username == user.username, User.email == user.email)).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="User with username or email already exists")
  hashed = hash_password(user.password)
  userdict = user.model_dump(exclude={"confirm_password"})
  new_user = User(**{**userdict, "password" : hashed})
  session.add(new_user)
  session.commit()
  session.refresh(new_user)
  return new_user

def authenticate_user(form_data, session:Session):
  user = session.query(User).filter(User.email == form_data.username).first()
  if not user:
    raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate":"Bearer"})
  if not check_password_hash(form_data.password, user.password):
    raise HTTPException(status_code=401, detail="Invalid Credentials", headers={"WWW-Authenticate":"Bearer"})
  payload = {"username":user.username}
  token = create_token(payload)
  return token

  