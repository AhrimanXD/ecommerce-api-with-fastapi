from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserCreate, UserOut
from app.services.user_services import create_user, authenticate_user
from app.db.database import SessionDep
from app.auth.dependencies import get_current_user, get_admin_user
from typing import Annotated
from app.models.users import User

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: SessionDep):
  new_user = create_user(user, db)
  return new_user


@router.post("/login")
async def login(db:SessionDep, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
  token = authenticate_user(form_data, db)
  return {"access_token":token,"token_type":"bearer"}

@router.get("/secret")
async def secret(current_user: Annotated[User,Depends(get_current_user)]):
  return {"message":f"Hello {current_user.username}"}

@router.get("/admin_secret")
async def admin_secret(admin_user: Annotated[User,Depends(get_admin_user)]):
  return {"message":f"Hello {admin_user.username} I hope all is well"}
