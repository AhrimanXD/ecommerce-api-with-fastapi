from fastapi import APIRouter, Query, Depends
from app.schemas.products import ProductCreate, ProductOut,ProductQuerySchema, ProductUpdate
from app.db.database import SessionDep
from app.services import product_services
from typing import Annotated
from app.models.users import User
from app.auth.dependencies import get_admin_user

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', response_model=list[ProductOut])
async def product_list(
  db: SessionDep,
  query:Annotated[ProductQuerySchema, Query()]
  ):
  return product_services.read_products(db, query)

@router.get('/{product_id}/', response_model=ProductOut, status_code=200)
async def product_detail(product_id: int, db: SessionDep):
  product = product_services.read_product(db, product_id)
  return product

@router.post('/', response_model=ProductOut, status_code=201)
async def create_product(product: ProductCreate, db: SessionDep, admin: Annotated[User, Depends(get_admin_user)]):
  return product_services.create_product(product, db)

@router.patch('/{product_id}/', response_model = ProductOut)
async def update_product(product_id: int, product: ProductUpdate, db: SessionDep, admin: Annotated[User, Depends(get_admin_user)]):
  response = product_services.update_product(product_id, product, db)
  return response

@router.delete('/{product_id}/', status_code=204)
async def delete_product(product_id: int, db: SessionDep, admin: Annotated[User, Depends(get_admin_user)]):
  response = product_services.delete_product(product_id, db)
  return response