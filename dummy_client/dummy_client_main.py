import time

import grpc

from dummy_client.header_interceptor import HeaderAdderInterceptor
from dummy_client.interceptor import Interceptor
from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc, service_pb2_grpc, service_pb2

grpc_server = 'localhost:8080'


class PublicClient:
    def __init__(self):
        self.name = "Andre (Public)"
        self.say_public()
        self.say_user()
        self.say_admin()

    def say_public(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayPublic(service_pb2.sayRequest(name=self.name)))

    def say_user(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayUser(service_pb2.sayRequest(name=self.name)))

    def say_admin(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayAdmin(service_pb2.sayRequest(name=self.name)))


class UserClient:
    def __init__(self):
        self.name = "Andre (User)"
        self.access_token = ""
        self.refresh_token = ""
        self.say_public()
        self.login("user", "user")
        time.sleep(10)
        self.say_user()
        self.say_admin()

    def login(self, username: str, password: str):
        with grpc.insecure_channel(grpc_server) as ch:
            resp = grpc_auth_pb2_grpc.AuthServiceStub(ch).login(grpc_auth_pb2.loginRequest(
                username=username,
                password=password))
            self.access_token = resp.access_token
            self.refresh_token = resp.refresh_token

    def say_public(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayPublic(service_pb2.sayRequest(name=self.name)))

    def say_user(self):
        header_adder_interceptor = HeaderAdderInterceptor('access_token', self.access_token).create()
        with grpc.insecure_channel(grpc_server) as ch:
            intercept_ch = grpc.intercept_channel(ch, header_adder_interceptor)
            print(service_pb2_grpc.ServiceStub(intercept_ch).sayUser(service_pb2.sayRequest(name=self.name)))

    def say_admin(self):
        header_adder_interceptor = HeaderAdderInterceptor('access_token', self.access_token).create()
        with grpc.insecure_channel(grpc_server) as ch:
            intercept_ch = grpc.intercept_channel(ch, header_adder_interceptor)
            print(service_pb2_grpc.ServiceStub(intercept_ch).sayAdmin(service_pb2.sayRequest(name=self.name)))


class AdminClient:
    def __init__(self):
        self.interceptor = None
        self.name = "Andre (Admin)"

        try:
            self.say_public()
            self.say_with_credential(username="admin", password="admin")
        except Exception as e:
            print(e.__str__())
        finally:
            if self.interceptor is not None:
                self.interceptor.close()

    def say_public(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayPublic(service_pb2.sayRequest(name=self.name)))

    def say_with_credential(self, username: str, password: str):
        with grpc.insecure_channel(grpc_server) as ch:
            resp = grpc_auth_pb2_grpc.AuthServiceStub(ch).login(grpc_auth_pb2.loginRequest(
                username=username,
                password=password))
            self.interceptor = Interceptor(grpc_server, resp.access_token, resp.refresh_token)

            intercept_ch = grpc.intercept_channel(ch, self.interceptor.create())
            for cnt in range(0, 101):
                time.sleep(10.0)
                print(f"{cnt} - "
                      f"{service_pb2_grpc.ServiceStub(intercept_ch).sayUser(service_pb2.sayRequest(name=self.name))}")

                time.sleep(5.0)
                print(f"{cnt} - "
                      f"{service_pb2_grpc.ServiceStub(intercept_ch).sayAdmin(service_pb2.sayRequest(name=self.name))}")


if __name__ == '__main__':
    # PublicClient()
    # UserClient()
    AdminClient()
