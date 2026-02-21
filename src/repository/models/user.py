from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users' # Name of the table in the database

    # Define columns for the users table
    user_id = Column("user_id", Sequence('user_id_seq', start=2, increment=1), primary_key=True)
    username = Column("username", String)
    name = Column("name", String)
    email = Column("email", String)

    # Define a string representation for the User class
    def __repr__(self):
        return f"<User(id={self.user_id}, username='{self.username}' , name='{self.name}', email='{self.email}')>"