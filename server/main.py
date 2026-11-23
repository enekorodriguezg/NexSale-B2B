from fastapi import FastAPI
import logging

from .routers import orders, products, auth
from .database import Base, engine
from scripts.seed_users import seed_database

### --------------------------------------------------###

logging.basicConfig(level = logging.INFO, format = "%(asctime)s %(levelname)s %(name)s: %(message)s")
Base.metadata.create_all(bind = engine)
seed_database()

app = FastAPI(
    title = "NexSale-B2B",
    description = "Backend transaccional para gestión de pedidos y ventas B2B",
    version = "1.0.0"
)

#Routers
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(auth.router)


@app.get("/health", tags = ["health"])
def health_check():
    return {"status": "ok", "app": "NexSale-B2B"}