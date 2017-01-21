from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    name = Column(String(80), nullable=False)
    email = Column(String(80))
    phone = Column(String(20))
    picture = Column(String(250))
    id = Column(Integer, primary_key=True)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id':   self.id,
        }


class Product(Base):
    __tablename__ = 'product'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(10))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name':         self.name,
            'description':  self.description,
            'id':           self.id,
            'picture':      self.picture,
            'category id':  self.category_id,
            'price':        self.price,
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
