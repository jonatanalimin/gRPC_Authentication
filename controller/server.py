from concurrent import futures

import grpc

from remote_function import auth, service
from remote_function.proto import grpc_auth_pb2_grpc, service_pb2_grpc


class Server:
    def __init__(self):
        self.backend_server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        grpc_auth_pb2_grpc.add_AuthServiceServicer_to_server(auth.Auth(), self.backend_server)
        service_pb2_grpc.add_ServiceServicer_to_server(service.Service(), self.backend_server)
        self.backend_server.add_insecure_port("localhost:8080")

    def start(self):
        self.backend_server.start()
        self.backend_server.wait_for_termination()
