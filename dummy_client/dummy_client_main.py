import time

import grpc

from dummy_client.interceptor import Interceptor
from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc, service_pb2_grpc, service_pb2

grpc_server = 'localhost:8080'


class PublicClient:
    def __init__(self):
        self.name = "Andre (Public)"
        self.say_public()

    def say_public(self):
        with grpc.insecure_channel(grpc_server) as ch:
            print(service_pb2_grpc.ServiceStub(ch).sayPublic(service_pb2.sayRequest(name=self.name)))


class UserClient:
    def __init__(self):
        self.interceptor = None
        self.name = "Andre (User)"
        try:
            self.say_public()
            self.say_with_credential(username="user", password="user")
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

            for cnt in range(0, 2):
                time.sleep(10.0)
                print(f"{cnt} - "
                      f"{service_pb2_grpc.ServiceStub(intercept_ch).sayUser(service_pb2.sayRequest(name=self.name))}")

            for response in service_pb2_grpc.ServiceStub(intercept_ch) \
                    .sayUnaryStream(service_pb2.sayRequest(name=self.name)):
                print(response)

            print(service_pb2_grpc.ServiceStub(intercept_ch).sayStreamUnary(self.stream_request()))

            for response in service_pb2_grpc.ServiceStub(intercept_ch).sayStreamStream(self.stream_request()):
                print(response)

    @staticmethod
    def stream_request():
        for name in ["Messi", "Diaz", "Ronaldo",
                     "Juergen", "Klopp", "Joeachim", "Klauus"]:
            time.sleep(1.0)
            yield service_pb2.sayRequest(name=name)


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

            for cnt in range(0, 2):
                time.sleep(10.0)
                print(f"{cnt} - "
                      f"{service_pb2_grpc.ServiceStub(intercept_ch).sayUser(service_pb2.sayRequest(name=self.name))}")

                time.sleep(5.0)
                print(f"{cnt} - "
                      f"{service_pb2_grpc.ServiceStub(intercept_ch).sayAdmin(service_pb2.sayRequest(name=self.name))}")

            for response in service_pb2_grpc.ServiceStub(intercept_ch) \
                    .sayUnaryStream(service_pb2.sayRequest(name=self.name)):
                print(response)

            print(service_pb2_grpc.ServiceStub(intercept_ch).sayStreamUnary(self.stream_request()))

            for response in service_pb2_grpc.ServiceStub(intercept_ch).sayStreamStream(self.stream_request()):
                print(response)

    @staticmethod
    def stream_request():
        for name in ["Messi", "Diaz", "Ronaldo",
                     "Juergen", "Klopp", "Joeachim", "Klauus"]:
            time.sleep(1.0)
            yield service_pb2.sayRequest(name=name)


if __name__ == '__main__':
    # PublicClient()
    # UserClient()
    AdminClient()
