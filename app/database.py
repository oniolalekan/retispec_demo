from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
#from .config import settings


# setup connection string to connect to the postgre DB
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Pa%%w0rd1@localhost/postgres'  #f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine =  create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#create session to the DB at every api call. It's passed to the path
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()