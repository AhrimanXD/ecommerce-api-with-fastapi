from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings 
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends

engine = create_engine(settings.DATABASE_URL, echo=settings.DEV, pool_pre_ping=True, pool_recycle=300, pool_size=10, max_overflow=20, pool_timeout=30)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

SessionDep = Annotated[Session, Depends(get_db)]

class Base(DeclarativeBase):
  pass
