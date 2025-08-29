from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String



class Category(Base):
  __tablename__ = 'categories'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(35), index=True, unique=True)
  products: Mapped[list['Product']] = relationship(back_populates='category')
