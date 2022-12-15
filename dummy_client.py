import grpc

from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc

grpc_server = 'localhost:8080'


def login(username: str, password: str):
    with grpc.insecure_channel(grpc_server) as ch:
        print(grpc_auth_pb2_grpc.AuthServiceStub(ch).login(grpc_auth_pb2.loginRequest(username=username,
                                                                                      password=password)))


if __name__ == '__main__':
    login("admin", "admin")
