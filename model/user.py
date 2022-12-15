from sqlalchemy import Column, Integer, String

from model import Base


class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, unique=True)
