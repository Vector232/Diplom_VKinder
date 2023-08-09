import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from vkinderdbmodel import create_tables, User, Photo, Output, Photo_User

def load_dsn():
    load_dotenv()

    dialect = os.getenv('dialect')
    driver = os.getenv('driver')
    login = os.getenv('login_DB')
    password = os.getenv('password_DB')
    server_name = os.getenv('server_name')
    port = os.getenv('port') 
    db_name = os.getenv('db_name')
    
    return f'{dialect}+{driver}://{login}:{password}@{server_name}:{port}/{db_name}'


DSN = load_dsn()
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

