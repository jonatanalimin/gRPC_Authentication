import logging
import time

from remote_function.proto import service_pb2, service_pb2_grpc

logger = logging.getLogger(__name__)


class Service(service_pb2_grpc.ServiceServicer):
    """
    gRPC trial's service class
    """
    def __init__(self):
        # TODO document why this method is empty
        pass

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

    def sayStream(self, request, context):
        """
        SayStream service which can be accessed by role admin
        :param request: (object) proto consist (str) name
        :param context:
        :return: (object) proto consist (str) reply
        """
        logger.info("Get request say stream")
        name = request.name
        for n in range(0, 10):
            time.sleep(1.0)
            yield service_pb2.sayResponse(
                reply=f"Stream-{n}: Hi {name}"
            )
