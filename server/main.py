from fastapi import FastAPI

from .routers import orders
from .database import Base, engine

### --------------------------------------------------###

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "NexSale-B2B",
    description = "Backend transaccional para gestión de pedidos y ventas B2B",
    version = "1.0.0"
)

#Routers
app.include_router(orders.router)


@app.get("/health", tags = ["health"])
def health_check():
    return {"status": "ok", "app": "NexSale-B2B"}