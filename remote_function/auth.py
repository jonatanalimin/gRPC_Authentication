import grpc

from service.jwt_manager import JWTManager
from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc
from repository.user import UserRepository


class Auth(grpc_auth_pb2_grpc.AuthServiceServicer):
    def __init__(self):
        self.jwt_manager = JWTManager()

    def login(self, request, context):
        user_repo = UserRepository()
        success, detail, user_object = user_repo.login(request.username, request.password)
        if success:
            return grpc_auth_pb2.loginResponse(
                access_token=self.jwt_manager.create_jwt(user_object))
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        context.set_details(detail)
        return grpc_auth_pb2.loginResponse()
