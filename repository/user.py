import bcrypt as bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.user import UserModel
from repository import application_path


class UserRepository:
    def __init__(self):
        engine = create_engine(f"sqlite:///{application_path}/grpc_auth.db")
        session_ = sessionmaker()
        session_.configure(bind=engine)
        self.session = session_()

    def get_all(self):
        return self.session.query(UserModel).all()

    def find_user(self, username: str):
        return self.session.query(UserModel)\
            .filter(UserModel.username == username)\
            .first()

    def login(self, username: str, password: str):
        user = self.find_user(username)
        if user is not None:
            if self.password_is_valid(password, user.password):
                return True, "", user
            else:
                return False, "Invalid password!", None
        else:
            return False, f"User {username} not found!", None

    @staticmethod
    def password_is_valid(password_params: str, stored_password: str):
        return True if bcrypt.checkpw(password_params.encode('utf-8'), stored_password.encode('utf-8')) else False
