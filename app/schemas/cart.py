from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from typing import Optional


# Request Schemas
class AddToCartRequest(BaseModel):
  product_id: int = Field(gt=0, description="ID of the product to add to cart")
  quantity: int = Field(default=1, ge=1, le=100, description="Quantity to add (1-100)")


class UpdateCartItemRequest(BaseModel):
  quantity: int = Field(ge=1, le=100, description="New quantity (1-100)")


# Response Schemas
class CartItemResponse(BaseModel):
  product_id: int
  product_name: str
  product_price: Decimal
  quantity: int
  subtotal: Decimal
  
  model_config = {"from_attributes": True}


class CartResponse(BaseModel):
  items: list[CartItemResponse]
  total_items: int
  total_amount: Decimal
  
  @field_validator('total_amount')
  @classmethod
  def round_total(cls, v):
    return round(v, 2)


class CartItemOut(BaseModel):
  """Legacy schema for backward compatibility"""
  name: str
  price: float
  quantity: int
  sub_total: float


class CartOperationResponse(BaseModel):
  message: str
  success: bool = True

