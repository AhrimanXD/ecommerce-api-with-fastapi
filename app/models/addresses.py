from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


from app.db.database import Base


class Address(Base):
  __tablename__ = 'addresses'

  id: Mapped[int] = mapped_column(primary_key=True)
  country: Mapped[str] = mapped_column(String(70), index=True)
  state: Mapped[str] = mapped_column(String(70), index=True)
  address: Mapped[str] = mapped_column(String(255))
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
  user: Mapped['User'] = relationship(back_populates='addresses')

class PhoneNumber(Base):
  __tablename__ = 'phonenumbers'

  id: Mapped[int] = mapped_column(primary_key=True)
  phonenumber: Mapped[str] = mapped_column(String(30), unique=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
  user: Mapped['User'] = relationship(back_populates='phonenumbers')