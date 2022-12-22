import logging
import time

from remote_function.proto import service_pb2, service_pb2_grpc

logger = logging.getLogger(__name__)


class Service(service_pb2_grpc.ServiceServicer):
    """
    gRPC trial's service class
    """
    def sayPublic(self, request, context):
        """
        SayPublic service which can be accessed by public/all user
        :param request: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        logger.info("Get request say public")
        return service_pb2.sayResponse(
            reply=f"Public: Hi {request.name}")

    def sayUser(self, request, context):
        """
        SayUser service which can be accessed by role user/admin
        :param request: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        logger.info("Get request say user")
        return service_pb2.sayResponse(
            reply=f"User: Hi {request.name}")

    def sayAdmin(self, request, context):
        """
        SayAdmin service which can be accessed by role admin
        :param request: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        logger.info("Get request say admin")
        return service_pb2.sayResponse(
            reply=f"Admin: Hi {request.name}")

    def sayUnaryStream(self, request, context):
        """
        SayUnaryStream service which can be accessed by role user, admin
        :param request: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        logger.info("Get request say stream")
        name = request.name
        for n in range(0, 10):
            time.sleep(1.0)
            yield service_pb2.sayResponse(
                reply=f"Unary Stream-{n}: Hi {name}"
            )

    def sayStreamUnary(self, request_iterator, context):
        """
        SayStreamUnary service which can be accessed by role admin
        :param request_iterator: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        reply = "Stream Unary: Hi "
        for request in request_iterator:
            reply = reply + f"{request.name}, "
        return service_pb2.sayResponse(
                reply=reply
        )

    def sayStreamStream(self, request_iterator, context):
        """
        SayStreamStream service which can be accessed by role admin
        :param request_iterator: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        for request in request_iterator:
            yield service_pb2.sayResponse(
                reply=f"Stream Stream : Hi {request.name}"
            )
