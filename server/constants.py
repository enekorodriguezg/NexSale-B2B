from enum import Enum

### --------------------------------------------------###

class UserRole(str, Enum):
    COMMERCIAL = "commercial"
    ADMIN = "admin"
    WAREHOUSE = "warehouse"