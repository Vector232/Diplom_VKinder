import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from vkinderdbmodel import create_tables, push, User, Photo, Output, Photo_User

class DateBase:
    def __init__(self) -> None:
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

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def push_card(self, data):
        push(self.session, data)
        print(self.session.query(User).all())

print('lol')