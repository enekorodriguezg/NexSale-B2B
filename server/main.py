from fastapi import FastAPI
import logging

from .routers import order_router, product_router, auth_router, user_router, settings_router, security_router, supplier_router, carrier_router
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
app.include_router(order_router.router)
app.include_router(product_router.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(settings_router.router)
app.include_router(security_router.router)
app.include_router(supplier_router.router)
app.include_router(carrier_router.router)


@app.get("/health", tags = ["health"])
def health_check():
    return {"status": "ok", "app": "NexSale-B2B"}