import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

user=os.getenv("MYSQL_USER")
password=os.getenv("MYSQL_PASSWORD")
database=os.getenv("MYSQL_DATABASE")
port=os.getenv("MYSQL_PORT")

DATABASE_URL=f"mysql+pymysql://{user}:{password}@localhost:{port}/{database}"

engine=create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal=sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()