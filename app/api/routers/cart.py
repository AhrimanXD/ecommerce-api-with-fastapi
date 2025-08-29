from fastapi import APIRouter, Depends, HTTPException, Body
from app.auth.dependencies import get_current_user
from typing import Annotated, Union
from app.models.users import User
from app.db.database import SessionDep
from app.services import cart_services
from app.schemas.cart import CartItemOut

router = APIRouter(prefix='/cart', tags=['cart'])


@router.post('/add/', status_code=201)
async def add_to_cart(product_id: Annotated[int, Body()], current_user: Annotated[User, Depends(get_current_user)], db: SessionDep):
  try:
    success = cart_services.add_to_cart(db, current_user, product_id)
    if success:
      return {"message": "Product added to cart successfully"}
    else:
      raise HTTPException(status_code=400, detail="Failed to add product to cart")
  except Exception as e:
    raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get('/', status_code=200, response_model=Union[list[CartItemOut], None])
async def get_cart(current_user: Annotated[User, Depends(get_current_user)], db: SessionDep):
  return cart_services.get_cart(db, current_user)