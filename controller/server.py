import configparser
import logging
from concurrent import futures

import grpc

from remote_function import auth, service
from remote_function.proto import grpc_auth_pb2_grpc, service_pb2_grpc
from service.jwt_manager import JWTManager

logger = logging.getLogger(__name__)


class AuthorizationInterceptors(grpc.ServerInterceptor):
    """
    Interceptor Server-Side
    To check authorization
    """
    def __init__(self):
        self.jwt_manager = JWTManager()

        # the gRPC function which only can access by role admin/user
        self.unary_unary_function = {
            "/Service/sayUser": ["admin", "user"],
            "/Service/sayAdmin": ["admin"]
        }
        self.unary_stream_function = {
            "/Service/sayUnaryStream": ["admin", "user"]
        }
        self.stream_unary_function = {
            "/Service/sayStreamUnary": ["admin"]
        }
        self.stream_stream_function = {
            "/Service/sayStreamStream": ["admin"]
        }
        self.list_function = self.unary_unary_function | self.unary_stream_function | self.stream_unary_function \
            | self.stream_stream_function

    def terminator(self, method, code, details):
        """
        Function to terminate client request, before execute the gRPC function
        :param method: (str) the target function name
        :param code: (str) the abort code
        :param details: (str) the abort detail
        :return: (object) an RpcMethodHandler object that is typically used by grpc.Server.
        """
        if method in self.unary_unary_function.keys():
            return self._unary_unary_rpc_terminator(code, details)
        elif method in self.unary_stream_function.keys():
            return self._unary_stream_rpc_terminator(code, details)
        elif method in self.stream_unary_function.keys():
            return self._stream_unary_rpc_terminator(code, details)
        else:
            return self._stream_stream_rpc_terminator(code, details)

    @staticmethod
    def _unary_unary_rpc_terminator(code, details):
        """
        Unary-Unary terminator
        :param code: (str) the abort code
        :param details: (str) the abort detail
        :return: (object) an RpcMethodHandler object that is typically used by grpc.Server.
        """
        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.unary_unary_rpc_method_handler(terminate)

    @staticmethod
    def _unary_stream_rpc_terminator(code, details):
        """
        Unary-Stream terminator
        :param code: (str) the abort code
        :param details: (str) the abort detail
        :return: (object) an RpcMethodHandler object that is typically used by grpc.Server.
        """
        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.unary_stream_rpc_method_handler(terminate)

    @staticmethod
    def _stream_unary_rpc_terminator(code, details):
        """
        Stream-Unary terminator
        :param code: (str) the abort code
        :param details: (str) the abort detail
        :return: (object) an RpcMethodHandler object that is typically used by grpc.Server.
        """

        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.stream_unary_rpc_method_handler(terminate)

    @staticmethod
    def _stream_stream_rpc_terminator(code, details):
        """
        Stream-Stream terminator
        :param code: (str) the abort code
        :param details: (str) the abort detail
        :return: (object) an RpcMethodHandler object that is typically used by grpc.Server.
        """

        def terminate(ignored_request, context):
            context.abort(code, details)

        return grpc.stream_stream_rpc_method_handler(terminate)

    def intercept_service(self, continuation, handler_call_details):
        """
        Implement the abstract function of grpc.ServerInterceptor class;
        :param continuation: A function that takes a HandlerCallDetails and proceeds to invoke the next interceptor in
        the chain, if any, or the RPC handler lookup logic, with the call details passed as an argument, and returns an
        RpcMethodHandler instance if the RPC is considered serviced, or None otherwise;
        :param handler_call_details: A HandlerCallDetails describing the RPC
        :return: An RpcMethodHandler with which the RPC may be serviced if the interceptor chooses to service this RPC,
        or None otherwise.
        """
        token, header = None, None
        logger.debug("Intercept a request")
        if handler_call_details.method in self.list_function.keys():
            for metadata in handler_call_details.invocation_metadata:
                if metadata.key == "access_token":
                    token = metadata.value

            if token is not None:
                try:
                    header = self.jwt_manager.verify_jwt_access(token)
                except Exception as e:
                    logger.warning("Get an unauthenticated request (token unverified)!")
                    return self.terminator(handler_call_details.method,
                                           grpc.StatusCode.UNAUTHENTICATED,
                                           e.__str__())
                if header.get("role") not in self.list_function.get(handler_call_details.method):
                    logger.warning("Get an unauthenticated request (authorization rejected)!")
                    return self.terminator(handler_call_details.method,
                                           grpc.StatusCode.UNAUTHENTICATED,
                                           "You don't have permission")
            else:
                logger.warning("Get an unauthenticated request (no access token)!")
                return self.terminator(handler_call_details.method,
                                       grpc.StatusCode.UNAUTHENTICATED,
                                       "Need token!")

        logger.info(f"Continuing to function {handler_call_details.method}")
        return continuation(handler_call_details)


class Server:
    """
    Server of The gRPC trial
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/configuration.ini')

        self.backend_server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=int(self.config['MIDDLEWARE']['worker_thd'])),
            interceptors=(AuthorizationInterceptors(),)
        )
        grpc_auth_pb2_grpc.add_AuthServiceServicer_to_server(auth.Auth(), self.backend_server)
        service_pb2_grpc.add_ServiceServicer_to_server(service.Service(), self.backend_server)
        self.backend_server.add_insecure_port(self.config['MIDDLEWARE']['server_addr'])

    def start(self):
        """
        Starting the gRPC Trial server
        :return:
        """
        logger.info("Starting gRPC server...")
        self.backend_server.start()
        logger.info("gRPC server started")
        self.backend_server.wait_for_termination()
