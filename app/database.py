from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras  import RealDictCursor
# import time

# password=quote_plus("Harsha@123") #used quote_plus to parse the special character @
# SQLAlchemy_database_url=f'postgresql://postgres:{password}@localhost:5432/fastapi'

encoded_password=quote_plus(settings.database_password)
SQLAlchemy_database_url=f'postgresql://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLAlchemy_database_url) #responsible for connection to daatabse

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
#for session management with db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#To connect to postgressql using python library (psycopg2) can be used while dealing with records in a array form
# while True: # to try making connection until it makes a db connection
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',
#                                 user='postgres',password='Harsha@123',
#                                 cursor_factory=RealDictCursor)
#         cursor =conn.cursor()
#         print('DB connection was successful')
#         break
#     except Exception as error:
#         print ("There is an error:",error)
#         time.sleep(2)
