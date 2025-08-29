from app.schemas.products import ProductCreate, ProductQuerySchema, ProductUpdate, ProductOut
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.products import Product
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .utils import exists
from app.core.redis import get_cache, set_cache, delete_cache
import logging

logger = logging.getLogger(__name__)

def create_product(product:ProductCreate, session:Session):
  db_product = Product(**product.model_dump())
  
  try:
    session.add(db_product)
    session.commit()
    delete_cache("products-*")
    logger.info(f"Cache invalidated and product created: {db_product.name}")
    session.refresh(db_product)
    return db_product
  except IntegrityError:
    session.rollback()
    raise HTTPException(status_code=409, detail='Product with name already exists')
  

def read_products(session:Session, query: ProductQuerySchema):
  cache_key = f"products-{query.q}-{query.skip}-{query.limit}"
  cached_products = get_cache(cache_key)
  if cached_products:
    logger.info("Cache hit for key: %s", cache_key)
    return cached_products
  
  logger.debug(f"Cache miss for key: {cache_key}. Querying database.")
  products = session.query(Product).filter(Product.is_available == True)
  if query.q:
    products = products.filter(or_(Product.name.icontains(query.q),Product.description.icontains(query.q)))
  products = products.offset(query.skip).limit(query.limit)
  
  set_cache(cache_key, [ProductOut.model_validate(product).model_dump() for product in products], ttl=600)
  return products


def read_product(session: Session, product_id: int):
  cache_key = f"product-{product_id}"
  cached_product = get_cache(cache_key)
  if cached_product:
    logger.info("Cache hit for key: %s", cache_key)
    return cached_product
  
  logger.debug(f"Cache miss for key: {cache_key}. Querying database.")
  product = session.get(Product, product_id)
  if not product:
    raise HTTPException(
      status_code=404,
      detail='Product Not Found'
    )
  set_cache(cache_key, ProductOut.model_validate(product).model_dump(), ttl=600)
  return product

def update_product(id: int, product: ProductUpdate, session: Session):
  old_product = session.get(Product, id)
  if not old_product:
    raise HTTPException(
      status_code=404,
      detail="Product not found"
    )
  for key, value in product.model_dump(exclude_unset=True).items():
    setattr(old_product, key, value)
  session.commit()
  session.refresh(old_product)
  return old_product
    
def delete_product(id: int, session: Session):
  product = session.get(Product, id)
  if not product:
    raise HTTPException(
      status_code=404,
      detail="Product not found"
    )
  session.delete(product)
  session.commit()
  return {
    "message":'Successfully Deleted Product'
  }
   