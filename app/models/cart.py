from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from app.db.database import Base


class Cart(Base):
  __tablename__ = 'cart'

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, unique=True)

  items: Mapped[list['CartItem']] = relationship(back_populates='cart', cascade='all, delete-orphan')
  user: Mapped['User'] = relationship(back_populates='cart')

class CartItem(Base):
  __tablename__ = 'cartitems'
  __table_args__ = (
    CheckConstraint('quantity >= 1', name='quantity_constraint'),
    UniqueConstraint('product_id','cart_id', name="unique_item_per_cart")
  )

  id: Mapped[int] = mapped_column(primary_key=True)
  product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
  cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
  quantity: Mapped[int]

  cart: Mapped['Cart'] = relationship(back_populates='items')