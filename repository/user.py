import logging

import bcrypt as bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.user import UserModel
from repository import application_path

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self):
        engine = create_engine(f"sqlite:///{application_path}/grpc_auth.db")
        session_ = sessionmaker()
        session_.configure(bind=engine)
        self.session = session_()

    def get_all(self):
        """
        Get all user at db
        :return: list[(UserModel) user data]
        """
        logger.info("Getting all user...")
        return self.session.query(UserModel).all()

    def find_user(self, username: str):
        """
        Searching user by username
        :param username: (str) username
        :return: (UserModel) user data
        """
        logger.info(f"Searching user with username {username}...")
        return self.session.query(UserModel)\
            .filter(UserModel.username == username)\
            .first()

    def login(self, username: str, password: str):
        """
        Logining by check username and password at db
        :param username: (str) username of user
        :param password: (str) plain-text password of user
        :return: (bool) Success, (str) Error detail, (UserModel) user data
        """
        logger.info(f"Logining user with username: {username}; password: {password}")
        user = self.find_user(username)
        if user is not None:
            if self.password_is_valid(password, user.password):
                logger.info("Login success!")
                return True, "", user
            else:
                logger.warning("Invalid password!")
                return False, "Invalid password!", None
        else:
            logger.warning(f"User {username} not found!")
            return False, f"User {username} not found!", None

    @staticmethod
    def password_is_valid(password_params: str, stored_password: str):
        """
        Validating given password
        :param password_params: (str) plain-text password which submitted at request
        :param stored_password: (str) Bcrypt encrypted hash password which saved at db
        :return: (bool) password valid
        """
        logger.info("Checking password...")
        return True if bcrypt.checkpw(password_params.encode('utf-8'), stored_password.encode('utf-8')) else False
