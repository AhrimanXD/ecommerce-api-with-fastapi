from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, DateTime
from sqlalchemy.sql import func
from .addresses import Address, PhoneNumber
from app.db.database import Base
from datetime import datetime

class User(Base):

  __tablename__ = 'users'
  __table_args__ = (
    CheckConstraint(
      "length(username)>=3",
      name="username_min_length"
      ),
  )
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
  first_name: Mapped[str] = mapped_column(String(50))
  last_name: Mapped[str] = mapped_column(String(50))
  password: Mapped[str] = mapped_column(String(255)) # Hashed Passwords
  is_verified: Mapped[bool] = mapped_column(default=True)
  is_admin: Mapped[bool] = mapped_column(default=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
  addresses: Mapped[list['Address']] = relationship(back_populates='user')
  phonenumbers: Mapped[list['PhoneNumber']] = relationship(back_populates='user')
  cart: Mapped['Cart'] = relationship(back_populates='user')
