from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#GANTI KE POSTGRESQL


# DATABASE_USER = "postgres"
# DATABASE_PASSWORD = "pandu"
# DATABASE_URI = "128.199.151.55"
# DATABASE_NAME = "refiller"
#DATABASE_URI = 'postgresql://postgres:pandu@localhost/refiller'
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()