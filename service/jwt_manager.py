import calendar
import configparser
import os
import sys
import datetime
import jwt

from model.user import UserModel


class JWTManager:
    def __init__(self):
        self.key = "secret"
        self.config = configparser.ConfigParser()
        self.config.read((os.path.dirname(sys.executable) + "/config/configuration.ini")
                         if getattr(sys, 'frozen', False) else os.getcwd() + "/config/configuration.ini")
        self.expired_time = int(self.config['MIDDLEWARE']['token_expired'])

    def create_jwt(self, user: UserModel):
        return jwt.encode({
            "expired_at": calendar.timegm(
                (datetime.datetime.now() + datetime.timedelta(seconds=self.expired_time)).timetuple()
            ),
            "username": user.username,
            "role": user.role
        }, self.key, algorithm="HS256")

    def verify_jwt(self, access_token: str):
