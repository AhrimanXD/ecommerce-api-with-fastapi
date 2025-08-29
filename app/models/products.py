from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, CheckConstraint, ForeignKey, Numeric,Enum as SQLEnum
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime
from typing import Optional
from enum import Enum
from .categories import Category
class UnitEnum(str, Enum):
  KG = 'KG'
  G = "GRAM"
  LITER = "LITER"
  PIECE = 'PIECE'

class Product(Base):
  __tablename__ = 'products'

  __table_args__ = (
    CheckConstraint('price >= 0', name="price_constraints"),
    CheckConstraint('stock >= 0', name='stock_constraints')
  )

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
  category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), index=True)
  slug: Mapped[Optional[str]]
  description: Mapped[Optional[str]]
  price: Mapped[float] = mapped_column(Numeric(10, 2),index=True)
  stock: Mapped[int]
  size: Mapped[Optional[int]]
  unit: Mapped[Optional[UnitEnum]] = mapped_column(SQLEnum(UnitEnum,name="unit_enum",create_constraint = True, native_enum = False))
  is_available: Mapped[bool] = mapped_column(default=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  images : Mapped['ProductImage'] = relationship(back_populates='product')
  category: Mapped['Category'] = relationship(back_populates='products')


class ProductImage(Base):
  __tablename__ = 'productimages'

  id: Mapped[int] = mapped_column(primary_key=True)
  image: Mapped[Optional[bytes]]
  product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)
  product: Mapped['Product'] = relationship(back_populates='images')

  

