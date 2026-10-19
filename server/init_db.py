from .database import Base, engine
from .models import User, Product, Order, OrderItem

### --------------------------------------------------###

Base.metadata.drop_all(bind = engine)

Base.metadata.create_all(bind = engine)

print("Importacion correcta")