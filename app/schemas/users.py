from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from datetime import datetime

class UserBase(BaseModel):
  username: str = Field(min_length=3, max_length=30)
  email: EmailStr =  Field()
  first_name: str = Field(max_length=50)
  last_name: str = Field(max_length=50)


class UserCreate(UserBase):
  password: str = Field(min_length=8, max_length=128)
  confirm_password: str = Field(min_length=8, max_length=128)


  @field_validator("username")
  @classmethod
  def validate_username(cls, value: str):
    if not value.isalnum():
      raise ValueError("Username must contain only alphabets or numbers")
    return value
  

  @model_validator(mode="after")
  def validate_confirm_password(self):
    if self.password != self.confirm_password:
      raise ValueError("Password Mismatch!")
    return self

class UserLogin(BaseModel):
  username_or_email: str
  password: str = Field(min_length=1)


class UserEdit(UserBase):
  username: str | None = None
  email: EmailStr | None = None
  password: str | None = None
  first_name: str| None = None
  last_name: str| None = None

class UserOut(UserBase):
  created_at: datetime
  updated_at: datetime

  model_config = {"from_attributes":True}

