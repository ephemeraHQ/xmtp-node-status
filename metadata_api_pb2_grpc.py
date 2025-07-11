# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import metadata_api_pb2 as metadata__api__pb2

GRPC_GENERATED_VERSION = '1.73.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in metadata_api_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class MetadataApiStub(object):
    """Metadata for distributed tracing, debugging and synchronization
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetSyncCursor = channel.unary_unary(
                '/xmtp.xmtpv4.metadata_api.MetadataApi/GetSyncCursor',
                request_serializer=metadata__api__pb2.GetSyncCursorRequest.SerializeToString,
                response_deserializer=metadata__api__pb2.GetSyncCursorResponse.FromString,
                _registered_method=True)
        self.SubscribeSyncCursor = channel.unary_stream(
                '/xmtp.xmtpv4.metadata_api.MetadataApi/SubscribeSyncCursor',
                request_serializer=metadata__api__pb2.GetSyncCursorRequest.SerializeToString,
                response_deserializer=metadata__api__pb2.GetSyncCursorResponse.FromString,
                _registered_method=True)
        self.GetVersion = channel.unary_unary(
                '/xmtp.xmtpv4.metadata_api.MetadataApi/GetVersion',
                request_serializer=metadata__api__pb2.GetVersionRequest.SerializeToString,
                response_deserializer=metadata__api__pb2.GetVersionResponse.FromString,
                _registered_method=True)


class MetadataApiServicer(object):
    """Metadata for distributed tracing, debugging and synchronization
    """

    def GetSyncCursor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeSyncCursor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVersion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MetadataApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetSyncCursor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSyncCursor,
                    request_deserializer=metadata__api__pb2.GetSyncCursorRequest.FromString,
                    response_serializer=metadata__api__pb2.GetSyncCursorResponse.SerializeToString,
            ),
            'SubscribeSyncCursor': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeSyncCursor,
                    request_deserializer=metadata__api__pb2.GetSyncCursorRequest.FromString,
                    response_serializer=metadata__api__pb2.GetSyncCursorResponse.SerializeToString,
            ),
            'GetVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetVersion,
                    request_deserializer=metadata__api__pb2.GetVersionRequest.FromString,
                    response_serializer=metadata__api__pb2.GetVersionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'xmtp.xmtpv4.metadata_api.MetadataApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('xmtp.xmtpv4.metadata_api.MetadataApi', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MetadataApi(object):
    """Metadata for distributed tracing, debugging and synchronization
    """

    @staticmethod
    def GetSyncCursor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/xmtp.xmtpv4.metadata_api.MetadataApi/GetSyncCursor',
            metadata__api__pb2.GetSyncCursorRequest.SerializeToString,
            metadata__api__pb2.GetSyncCursorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeSyncCursor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/xmtp.xmtpv4.metadata_api.MetadataApi/SubscribeSyncCursor',
            metadata__api__pb2.GetSyncCursorRequest.SerializeToString,
            metadata__api__pb2.GetSyncCursorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/xmtp.xmtpv4.metadata_api.MetadataApi/GetVersion',
            metadata__api__pb2.GetVersionRequest.SerializeToString,
            metadata__api__pb2.GetVersionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
