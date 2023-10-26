from .database import Base
from sqlalchemy import Column,Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


#ORM/sqlalchemy Model: responsible for defining the postgresql db tables
class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default='True', nullable=False)
    createdAt=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id= Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    owner= relationship("User") #sqlalchemy is going to create a another property called owner and figures out the relationship with it's User class
    # here owner attribute is related to User class by a foreign key on users.id


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable= False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__="votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)






