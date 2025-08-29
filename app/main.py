from fastapi import FastAPI
from app.db.database import Base,engine
from app.api.routers import users, products, cart


app = FastAPI(
  title="Ecommerce API",
  summary="As The Name Implies it is an ecommerce api",
  version="1.0.0"
)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)

@app.on_event("startup")
def create_tables():
  Base.metadata.create_all(engine)