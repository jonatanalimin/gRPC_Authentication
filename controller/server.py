from concurrent import futures

import grpc

from remote_function import auth, service
from remote_function.proto import grpc_auth_pb2_grpc, service_pb2_grpc
from service.jwt_manager import JWTManager


class AuthorizationInterceptors(grpc.ServerInterceptor):
    def __init__(self):
        self.jwt_manager = JWTManager()
        self.list_function = {
            "/Service/sayUser": ["admin", "user"],
            "/Service/sayAdmin": ["admin"]
        }

    @staticmethod
    def _unary_unary_rpc_terminator(code, details):
        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.unary_unary_rpc_method_handler(terminate)

    def intercept_service(self, continuation, handler_call_details):
        token, header = None, None

        if handler_call_details.method in self.list_function.keys():
            for metadata in handler_call_details.invocation_metadata:
                if metadata.key == "access_token":
                    token = metadata.value

            if token is not None:
                try:
                    header = self.jwt_manager.verify_jwt_access(token)
                except Exception as e:
                    return self._unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, e.__str__())
                if header.get("role") not in self.list_function.get(handler_call_details.method):
                    return self._unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED,
                                                            "You don't have permission")
            else:
                return self._unary_unary_rpc_terminator(grpc.StatusCode.UNAUTHENTICATED, "Need token!")

        return continuation(handler_call_details)


class Server:
    def __init__(self):
        self.backend_server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=5),
            interceptors=(AuthorizationInterceptors(),)
        )
        grpc_auth_pb2_grpc.add_AuthServiceServicer_to_server(auth.Auth(), self.backend_server)
        service_pb2_grpc.add_ServiceServicer_to_server(service.Service(), self.backend_server)
        self.backend_server.add_insecure_port("localhost:8080")

    def start(self):
        self.backend_server.start()
        self.backend_server.wait_for_termination()
