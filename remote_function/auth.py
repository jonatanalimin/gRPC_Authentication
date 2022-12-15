from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc
from repository.user import UserRepository


class Auth(grpc_auth_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        # TODO document why this method is empty
        pass

    def login(self, request, context):
        user_repo = UserRepository()
        return grpc_auth_pb2.loginResponse(
            access_token=user_repo.login(request.username, request.password).__str__())
