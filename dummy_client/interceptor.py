import collections
import time
from threading import Timer

import grpc
import jwt

from dummy_client.generic_client_interceptors import _GenericClientInterceptor
from remote_function.proto import grpc_auth_pb2, grpc_auth_pb2_grpc


class Interceptor:
    def __init__(self, grpc_server, access_token, refresh_token):
        self.refreshing_token = False
        self.grpc_server = grpc_server
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.timer = Timer(7.5, self.on_refreshing_token)
        self.timer.start()

    def is_on_refreshing_token(self):
        return self.refreshing_token

    def on_refreshing_token(self):
        print("refreshing....")
        self.refreshing_token = True
        try:
            with grpc.insecure_channel(self.grpc_server) as ch:
                self.access_token = (grpc_auth_pb2_grpc.AuthServiceStub(ch).refreshing_token(
                    grpc_auth_pb2.refreshRequest(refresh_token=self.refresh_token))).access_token
        except jwt.exceptions.ExpiredSignatureError as e:
            raise InterceptorException(e.__str__())
        except Exception as e:
            print(e.__str__())
        finally:
            self.timer = Timer(7.5, self.on_refreshing_token)
            self.timer.start()
            self.refreshing_token = False

    def intercept_call(self, client_call_details, request_iterator, request_streaming,
                       response_streaming):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((
            "access_token",
            self.access_token,
        ))
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return client_call_details, request_iterator, None

    def create(self):
        while self.is_on_refreshing_token():
            print("on waiting....")
            time.sleep(0.1)

        return _GenericClientInterceptor(self.intercept_call)

    def close(self):
        self.timer.cancel()
        print("closing interceptor...")


class _ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass


class InterceptorException (Exception):
    pass
