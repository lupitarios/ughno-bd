from tokenize import String

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' # Name of the table in the database

    # Define columns for the users table
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    email = Column(String)

    # Define a string representation for the User class
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}' , name='{self.name}', email='{self.email}')>"