from fastapi import FastAPI, Request
from app.db.database import Base,engine
from app.api.routers import users, products, cart
import time

app = FastAPI(
  title="Ecommerce API",
  summary="As The Name Implies it is an ecommerce api",
  version="1.0.0"
)




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)



@app.on_event("startup")
def create_tables():
  Base.metadata.create_all(engine)