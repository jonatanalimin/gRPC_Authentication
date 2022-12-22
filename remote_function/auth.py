import logging

import grpc

from service.jwt_manager import JWTManager
from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc
from repository.user import UserRepository

logger = logging.getLogger(__name__)


class Auth(grpc_auth_pb2_grpc.AuthServiceServicer):
    """
    gRPC trial's Auth service class
    """
    def __init__(self):
        # TODO document why this method is empty
        pass

    def login(self, request, context):
        """
        The login service
        :param request: (object) proto consist (str) username & (str) password
        :param context:
        :return: (object) proto consist (str) access token & (str) refresh token
        """
        try:
            logger.info(f"Get login request with username: {request.username} - password: {request.password}")
            user_repo = UserRepository()
            success, detail, user_object = user_repo.login(request.username, request.password)
            if success:
                access_token, refresh_token = JWTManager().create_jwt(user_object)
                return grpc_auth_pb2.loginResponse(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(detail)
            return grpc_auth_pb2.loginResponse()
        except GeneratorExit:
            logger.warning("Client disconnected before the function execution finished!")
        except Exception as e:
            logger.error("Error when login", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(e.__str__())
            return grpc_auth_pb2.loginResponse()

    def refreshing_token(self, request, context):
        """
        The access token refresher function
        :param request: (object) proto consist (str) refresh_token
        :param context:
        :return: (object) proto consist (str) access token
        """
        try:
            logger.info("Get request to refresh the access token")
            try:
                return grpc_auth_pb2.refreshResponse(
                    access_token=JWTManager().refreshing_token(request.refresh_token)
                                                     )
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details(e.__str__())
                return grpc_auth_pb2.refreshResponse()
        except GeneratorExit:
            logger.warning("Client disconnected before the function execution finished!")
