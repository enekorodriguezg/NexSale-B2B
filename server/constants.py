from enum import Enum

### --------------------------------------------------###

class UserRole(str, Enum):
    COMMERCIAL = "commercial"
    ADMIN = "admin"
    WAREHOUSE = "warehouse"

class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    COMPLETED = "completed"