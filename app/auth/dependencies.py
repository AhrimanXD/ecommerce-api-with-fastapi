from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException
from app.auth.utils import decode_token
from app.models.users import User
from app.db.database import SessionDep

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token : Annotated[str, Depends(oauth2scheme)], db: SessionDep):
  username = decode_token(token)
  return db.query(User).filter(User.username == username).first()

async def get_admin_user(current_user: Annotated[User, Depends(get_current_user)]):
  if not current_user.is_admin:
    raise HTTPException(status_code=401, detail="Insufficient Permission", headers={"WWW-Authenticate":"Bearer"})
  return current_user