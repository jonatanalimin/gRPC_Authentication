import calendar
import configparser
import logging
import os
import sys
import datetime
import jwt

from model.user import UserModel
from utility.custom_error import JWTError

logger = logging.getLogger(__name__)


class JWTManager:
    """
    JWT Manager class which have function to create and verify JWT
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read((os.path.dirname(sys.executable) + "/config/configuration.ini")
                         if getattr(sys, 'frozen', False) else os.getcwd() + "/config/configuration.ini")
        self.algorithm = self.config["MIDDLEWARE"]["algorithm"]
        self.access_key = self.config["MIDDLEWARE"]["access_token_signature"]
        self.refresh_key = self.config["MIDDLEWARE"]["refresh_token_signature"]
        self.access_token_expired_time = int(self.config["MIDDLEWARE"]["access_token_expired"])
        self.refresh_token_expired_time = int(self.config["MIDDLEWARE"]["refresh_token_expired"])

    def create_jwt(self, user: UserModel):
        """
        Creating JWT access token and refresh token when user login
        :param user: (UserModel) User data
        :return: (str) access token, (str) refresh token
        """
        return self.create_jwt_access(user), self.create_jwt_refresh(user)

    def create_jwt_access(self, user: UserModel):
        """
        Creating JWT Access Token
        :param user: (UserModel) user data
        :return: (str) Access Token
        """
        return jwt.encode({
            "exp": calendar.timegm(
                (datetime.datetime.utcnow() + datetime.timedelta(seconds=self.access_token_expired_time)).timetuple()
            ),
            "username": user.username,
            "role": user.role
        }, self.access_key, algorithm=self.algorithm)

    def create_jwt_refresh(self, user: UserModel):
        """
        Creating JWT Refresh Token
        :param user: (UserModel) user data
        :return: (str) Refresh Token
        """
        return jwt.encode({
                   "exp": calendar.timegm(
                       (datetime.datetime.utcnow() + datetime.timedelta(seconds=self.refresh_token_expired_time))
                       .timetuple()), "username": user.username, "role": user.role
               }, self.refresh_key, algorithm=self.algorithm)

    def verify_jwt_access(self, access_token: str):
        """
        Verifying access token
        :param access_token: (str) access token
        :return: dict(access token)
        """
        try:
            return(jwt.decode(access_token, self.access_key, self.algorithm, options={
                "verify_signature": True,
                "require": ["exp", "role"]
            }))
        except Exception as e:
            raise JWTError(e.__str__())

    def refreshing_token(self, refresh_token: str):
        """
        Creating new access token using refresh token
        :param refresh_token: (str) refresh token
        :return: (str) access token
        """
        try:
            data = jwt.decode(refresh_token, self.refresh_key, self.algorithm, options={
                "verify_signature": True,
                "require": ["exp", "username", "role"]
            })

            user = UserModel()
            user.username = data.get("username")
            user.role = data.get("role")

            return self.create_jwt_access(user)
        except Exception as e:
            raise JWTError(e.__str__())
