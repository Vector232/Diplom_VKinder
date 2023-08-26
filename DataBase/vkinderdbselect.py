import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from database.vkinderdbmodel import create_tables, User, Photo, Output, Photo_User

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

    def push_user_card(self, card):
        model = {'user': User,
                'photo': Photo,
                'photo_user' : Photo_User,
                'output': Output}[card.get('model')]

        self.session.add(model(user_id=card.get('user_id'), **card.get('fields')))

        self.session.commit()

    def push_photos(self, photos, user_id: int = -1):
        model = {'user': User,
                'photo': Photo,
                'photo_user' : Photo_User,
                'output': Output}[photos.get('model')]
        
        for photo in photos['fields']:
            self.session.add(model(photo_id=photo.get('photo_id'), url=photo.get('url')))
            if user_id != -1:
                self.session.add(Photo_User(photo_id=photo.get('photo_id'), user_id=user_id))

        self.session.commit()

        

        