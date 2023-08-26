import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.VARCHAR(length=20), nullable=False)
    last_name = sq.Column(sq.VARCHAR(length=20), nullable=False)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    relation = sq.Column(sq.Integer)
    city = sq.Column(sq.Integer)
    interest_table_id = sq.Column(sq.Integer)

    def __str__(self):
        return (f'User {self.user_id}: ({self.name, self.last_name}'
                f'{self.age, self.sex, self.relation, self.city, self.interest_table_id})')
    
class Photo(Base):
    __tablename__ = 'photo'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    url = sq.Column(sq.VARCHAR(length=300), nullable=False)

    def __str__(self):
        return f'Photo {self.photo_id}: ({self.url})'
    

class Photo_User(Base):
    __tablename__ = 'photo_user'

    photo_user_id = sq.Column(sq.Integer, primary_key=True)
    photo_id = sq.Column(sq.Integer, sq.ForeignKey('photo.photo_id'), nullable=False)
    user_id =  sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    photo = relationship(Photo, foreign_keys=[photo_id])
    user = relationship(User, foreign_keys=[user_id])

    def __str__(self):
        return f'Photo_User {self.photo_user_id}: ({self.photo_id, self.user_id})'
    
class Output(Base):
    __tablename__ = 'output'

    output_id = sq.Column(sq.Integer, primary_key=True)
    input_user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)
    output_user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    input_user = relationship(User, foreign_keys=[input_user_id])
    output_user = relationship(User, foreign_keys=[output_user_id])

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)