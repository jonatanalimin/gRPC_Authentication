from remote_function.proto import service_pb2, service_pb2_grpc


class Service(service_pb2_grpc.ServiceServicer):
    def __init__(self):
        # TODO document why this method is empty
        pass

    def sayPublic(self, request, context):
        return service_pb2.sayResponse(
            reply=f"Public: Hi {request.name}")

    def sayUser(self, request, context):
        return service_pb2.sayResponse(
            reply=f"User: Hi {request.name}")

    def sayAdmin(self, request, context):
        return service_pb2.sayResponse(
            reply=f"Admin: Hi {request.name}")
