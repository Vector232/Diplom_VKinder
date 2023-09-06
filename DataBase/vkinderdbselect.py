import os
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .vkinderdbmodel import create_tables, User, Photo, Output, Photo_User
from .vkinderdbmodel import Like, Photo_With_User, Blacklist, Whitelist
from logs.loger import Loger


class DateBase:
    def __init__(self, loger: Loger = None,new = True) -> None:
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
        self.log = loger
        if self.log: self.log.log(f'DB -> База данных создана.')
    
    # для дальнейшей стандартизации                                         ВСЕ ПЕРЕДЕЛАТЬ! РАЗДЕЛИТЬ! РАЗНЫЕ ВСТАВКИ - РАЗНЫЕ МЕТОДЫ!
    # все добавления в БД должны будут использлвать только этот метод
    def push(self, data: dict):
        def add_user():
            if self.session.query(User.user_id).where(User.user_id == data['fields']['user_id']).first():
                if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{data['fields']['user_id']} в User.")
            else:
                self.session.add(model(**data.get('fields')))
                
        def add_photo():
            if self.session.query(Photo.photo_id).where(Photo.photo_id == data['fields']['photo_id']).first():
                if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{data['fields']['photo_id']} в Photo.")
            else:
                self.session.add(model(photo_id=data['fields']['photo_id'], url=data['fields']['url']))
                if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{data['fields']['photo_id']} в Photo.")
            #  При создании фото, создается и связь фото с пользователем. 
            if self.session.query(Photo_User.photo_id).where(Photo_User.photo_id == data['fields']['photo_id']
                                                             and Photo_User.user_id == data['fields']['user_id']).first():
                if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{data['fields']['photo_id']} в Photo_User.")
            else:
                self.session.add(Photo_User(photo_id=data['fields']['photo_id'], user_id=data['fields']['user_id']))
                if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{data['fields']['photo_id']} и {data['fields']['user_id']} в Photo_User.")
        
        def add_photo_with_user():
            if self.session.query(Photo.photo_id).where(Photo.photo_id == data['fields']['photo_id']).first():
                if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{data['fields']['photo_id']} в Photo.")
            else:
                self.session.add(Photo(photo_id=data['fields']['photo_id'], url=data['fields']['url']))
                if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{data['fields']['photo_id']} в Photo.")
            #  При создании фото c пользователем, создается отдельная запись без привязки к владельца фото.
            if self.session.query(Photo_With_User.photo_id).where(Photo_With_User.photo_id == data['fields']['photo_id'] 
                                                                      and Photo_With_User.user_id == data['fields']['user_id']).first():
                if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{data['fields']['photo_id']} и {data['fields']['user_id']} в Photo_With_User.")
            else:
                if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{data['fields']['photo_id']} в Photo_With_User.")
                self.session.add(model(photo_id=data['fields']['photo_id'], user_id=data['fields']['user_id']))

        model = {'user': User,
                    'photo': Photo,
                    'photo_user': Photo_User,
                    'like': Like,
                    'output': Output,
                    'photo_with_user': Photo_With_User}[data.get('model')] #  Кажется уже ненужной. Пусть пока будет.
        
        if model is Photo:
            add_photo()
        elif model is Photo_With_User:
            add_photo_with_user()
        elif model is User:
            add_user()  
        else: #  Добавить проверок на User чтобы не было коллизий.                !!!!
            self.session.add(model(**data.get('fields')))
        self.session.commit()
    # для дальнейшей стандартизации
    # все простые запросы к БД должны будут использлвать только этот метод
    def get():
        pass

    def like_photo(self, user_id, photo_id):
        if self.session.query(Like.like_id).where(Like.photo_id == photo_id and Like.user_id == user_id).first():
            if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{user_id} и {photo_id} в Like.")
        else:
            self.session.add(Like(photo_id=photo_id, user_id=user_id))
            if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{user_id} и {photo_id} в Like.")
            self.session.commit()

    def push_to_balcklist(self, owner_id, banned_id):
        if self.session.query(Blacklist.blacklist_id).where(Blacklist.owner_user_id == owner_id and Blacklist.banned_user_id == banned_id).first():
            if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{owner_id} и {banned_id} в Blacklist.")
        else:
            self.session.add(Blacklist(owner_user_id=owner_id, banned_user_id=banned_id))
            if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{owner_id} и {banned_id} в Blacklist.")
            self.session.commit()

    def push_to_whitelist(self, owner_id, favor_id):
        if self.session.query(Whitelist.whitelist_id).where(Whitelist.owner_user_id == owner_id and Whitelist.favor_user_id == favor_id).first():
            if self.log: self.log.log(f"DB -> База данных уже содержит запись с ID:{owner_id} и {favor_id} в Whitelist.")
        else:
            self.session.add(Whitelist(owner_user_id=owner_id, favor_user_id=favor_id))
            if self.log: self.log.log(f"DB -> В базу данных добавлена запись запись с ID:{owner_id} и {favor_id} в Whitelist.")
            self.session.commit()

    def get_all_user_photos(self, id):
        res = []
        q = self.session.query(Photo.photo_id, Photo.url).select_from(Photo).join(Photo_User).where(Photo_User.user_id == id)
        for item in q:
            res.append(item)
        return res

    #  Или все-же использовать отдельные методы?
    def get_viewed(self, id):
        res = {}
        q = self.session.query(Output.output_user_id, Output.grade).where(Output.input_user_id == id)
        for item in q:
            res[item['output_user_id']] = item['grade']
        return res
    
    def get_blacklist(self, id):
        res = {}
        q = self.session.query(Blacklist.banned_user_id).where(Blacklist.owner_user_id == id)
        for item in q:
            res[item[0]] = 'BAN'
        return res
    
    def get_whitelist(self, id):
        res = {}
        q = self.session.query(Whitelist.favor_user_id).where(Whitelist.owner_user_id == id)
        for item in q:
            res[item[0]] = 'FAVOR'
        return res
    
    def get_users(self):
        res = []

        q = self.session.query(User.user_id)
        for item in q:
            res.append(item)

        return res

        

        