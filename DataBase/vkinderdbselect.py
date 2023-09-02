import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .vkinderdbmodel import create_tables, User, Photo, Output, Photo_User, Like

class DateBase:
    def __init__(self, new = True) -> None:
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

        if new: create_tables(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    # для дальнейшей стандартизации
    # все добавления в БД должны будут использлвать только этот метод
    def push(self, data: dict):
        model = {'user': User,
                    'photo': Photo,
                    'photo_user': Photo_User,
                    'like': Like,
                    'output': Output}[data.get('model')]
        if model is Photo:
            # при создании фото, создается и связь фото с пользователем
            self.session.add(model(photo_id=data['fields']['photo_id'], url=data['fields']['url']))
            self.session.add(Photo_User(photo_id=data['fields']['photo_id'], user_id=data['fields']['user_id'])) # дописать добавление связей со всеми отмеченными на фото
        else:
            self.session.add(model(**data.get('fields')))
        self.session.commit()
    # для дальнейшей стандартизации
    # все простые запросы к БД должны будут использлвать только этот метод
    def get():
        pass

    #  Или все-же использовать отдельные методы?
    def get_viewed(self, id):
        res = {}

        q = self.session.query(Output.output_user_id, Output.grade).where(Output.input_user_id == id)
        for item in q:
            res[item['output_user_id']] = item['grade']

        return res
    
    def get_users(self):
        res = []

        q = self.session.query(User.user_id)
        for item in q:
            res.append(item)

        return res

        

        