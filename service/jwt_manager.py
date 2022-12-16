import calendar
import configparser
import os
import sys
import datetime
import jwt

from model.user import UserModel
from utility.custom_error import JWTError


class JWTManager:
    def __init__(self):
        self.key = "secret"
        self.config = configparser.ConfigParser()
        self.config.read((os.path.dirname(sys.executable) + "/config/configuration.ini")
                         if getattr(sys, 'frozen', False) else os.getcwd() + "/config/configuration.ini")
        self.expired_time = int(self.config["MIDDLEWARE"]["token_expired"])

    def create_jwt(self, user: UserModel):
        return jwt.encode({
            "exp": calendar.timegm(
                (datetime.datetime.utcnow() + datetime.timedelta(seconds=self.expired_time)).timetuple()
            ),
            "username": user.username,
            "role": user.role
        }, self.key, algorithm="HS256")

    def verify_jwt(self, access_token: str):
        try:
            return(jwt.decode(access_token, self.key, "HS256", options={
                "verify_signature": True,
                "require": ["exp", "role"]
            }))
        except Exception as e:
            raise JWTError(e.__str__())


if __name__ == '__main__':
    JWTManager().verify_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVkX2F"
                            "0IjoxNjgxMTU5MTE4LCJ1c2VybmFtZSI6ImFkbWluIn0.MZvyPan03"
                            "aOeRMgrB6nTAmtu539Y51az7YIa_zxA30Y")
