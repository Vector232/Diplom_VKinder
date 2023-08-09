import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, unique=True)
    name = sq.Column(sq.VARCHAR(length=20), nullable=False)
    second_name = sq.Column(sq.VARCHAR(length=20))
    surname = sq.Column(sq.VARCHAR(length=20), nullable=False)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.VARCHAR(length=10))
    family_status = sq.Column(sq.VARCHAR(length=20))
    city = sq.Column(sq.VARCHAR(length=30))
    interest_table_id = sq.Column(sq.Integer)

    def __str__(self):
        return (f'User {self.user_id}: ({self.name, self.second_name, self.surname}'
                f'{self.age, self.sex, self.family_status, self.city, self.interest_table_id})')
    
class Photo(Base):
    __tablename__ = 'photo'

    photo_id = sq.Column(sq.Integer, unique=True)
    url = sq.Column(sq.VARCHAR(length=100), nullable=False)

    def __str__(self):
        return f'Photo {self.photo_id}: ({self.url})'
    

class Photo_User(Base):
    __tablename__ = 'photo_user'

    photo_user_id = sq.Column(sq.Integer, primary_key=True)
    photo_id = sq.Column(sq.Integer, sq.ForeignKey('photo.photo_id'), nullable=False)
    user_id =  sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    photo = relationship(Photo, backref='stock')
    user = relationship(User, backref='stock')

    def __str__(self):
        return f'Photo_User {self.photo_user_id}: ({self.photo_id, self.user_id})'
    
class Output(Base):
    __tablename__ = 'output'

    output_id = sq.Column(sq.Integer, primary_key=True)
    input_user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)
    output_user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship(User, backref='stock')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)