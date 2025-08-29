from pydantic import BaseModel, Field
from typing import Optional, Annotated
from app.models.products import UnitEnum
from datetime import datetime



class ProductCreate(BaseModel):
  name: str
  description: Optional[str]
  category_id: int = Field(ge=0)
  price: float = Field(ge=0)
  stock: int = Field(ge=0)
  size: Optional[int]
  unit: Optional[UnitEnum]
  is_available: Optional[bool] = True

non_neg_int = Annotated[int, Field(ge=0)]
non_neg_float = Annotated[float, Field(ge=0)]

class ProductUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  category_id: Optional[non_neg_int] = None
  price: Optional[non_neg_float] = None
  stock: Optional[non_neg_int] = None
  size: Optional[int] = None
  unit: Optional[UnitEnum] = None
  

class ProductOut(BaseModel):
  id: int
  slug: Optional[str]
  name: str
  description: str
  category_id: int
  price: float
  stock: int
  size: Optional[int]
  unit: Optional[UnitEnum]
  is_available: Optional[bool]
  created_at: datetime
  updated_at: datetime
  images: Optional[bytes]
  model_config = {"from_attributes":True}

class ProductQuerySchema(BaseModel):
  q: Optional[str] = None
  skip: int = 0
  limit: int = 10