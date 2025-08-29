from pydantic import BaseModel


class CartItemOut(BaseModel):
  name: str
  price: float
  quantity: int
  sub_total: float




