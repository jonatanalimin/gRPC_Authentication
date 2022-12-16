import collections

import grpc

from dummy_client.generic_client_interceptors import _GenericClientInterceptor


class HeaderAdderInterceptor:
    def __init__(self, header_, value_):
        self.header = header_
        self.value = value_

    def intercept_call(self, client_call_details, request_iterator, request_streaming,
                       response_streaming):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((
            self.header,
            self.value,
        ))
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return client_call_details, request_iterator, None

    def create(self):
        return _GenericClientInterceptor(self.intercept_call)


class _ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass
