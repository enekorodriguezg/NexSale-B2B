import os
from dotenv import load_dotenv

### --------------------------------------------------###

load_dotenv()

PEPPER: str = os.getenv("PEPPER", "fallback_para_desarrollo")
SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_jwt_inseguro")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8 #8 hours sessions