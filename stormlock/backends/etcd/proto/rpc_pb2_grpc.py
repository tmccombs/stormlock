# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from stormlock.backends.etcd.proto import rpc_pb2 as stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2


class KVStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Range = channel.unary_unary(
                '/etcdserverpb.KV/Range',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeResponse.FromString,
                )
        self.Put = channel.unary_unary(
                '/etcdserverpb.KV/Put',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutResponse.FromString,
                )
        self.DeleteRange = channel.unary_unary(
                '/etcdserverpb.KV/DeleteRange',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeResponse.FromString,
                )
        self.Txn = channel.unary_unary(
                '/etcdserverpb.KV/Txn',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnResponse.FromString,
                )
        self.Compact = channel.unary_unary(
                '/etcdserverpb.KV/Compact',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionResponse.FromString,
                )


class KVServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Range(self, request, context):
        """Range gets the keys in the range from the key-value store.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Put(self, request, context):
        """Put puts the given key into the key-value store.
        A put request increments the revision of the key-value store
        and generates one event in the event history.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRange(self, request, context):
        """DeleteRange deletes the given range from the key-value store.
        A delete request increments the revision of the key-value store
        and generates a delete event in the event history for every deleted key.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Txn(self, request, context):
        """Txn processes multiple requests in a single transaction.
        A txn request increments the revision of the key-value store
        and generates events with the same revision for every completed request.
        It is not allowed to modify the same key several times within one txn.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Compact(self, request, context):
        """Compact compacts the event history in the etcd key-value store. The key-value
        store should be periodically compacted or the event history will continue to grow
        indefinitely.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KVServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Range': grpc.unary_unary_rpc_method_handler(
                    servicer.Range,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeResponse.SerializeToString,
            ),
            'Put': grpc.unary_unary_rpc_method_handler(
                    servicer.Put,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutResponse.SerializeToString,
            ),
            'DeleteRange': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteRange,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeResponse.SerializeToString,
            ),
            'Txn': grpc.unary_unary_rpc_method_handler(
                    servicer.Txn,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnResponse.SerializeToString,
            ),
            'Compact': grpc.unary_unary_rpc_method_handler(
                    servicer.Compact,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'etcdserverpb.KV', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KV(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Range(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.KV/Range',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.RangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.KV/Put',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.PutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteRange(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.KV/DeleteRange',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.DeleteRangeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Txn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.KV/Txn',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.TxnResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Compact(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.KV/Compact',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.CompactionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class LeaseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LeaseGrant = channel.unary_unary(
                '/etcdserverpb.Lease/LeaseGrant',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantResponse.FromString,
                )
        self.LeaseRevoke = channel.unary_unary(
                '/etcdserverpb.Lease/LeaseRevoke',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeResponse.FromString,
                )
        self.LeaseKeepAlive = channel.stream_stream(
                '/etcdserverpb.Lease/LeaseKeepAlive',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveResponse.FromString,
                )
        self.LeaseTimeToLive = channel.unary_unary(
                '/etcdserverpb.Lease/LeaseTimeToLive',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveResponse.FromString,
                )
        self.LeaseLeases = channel.unary_unary(
                '/etcdserverpb.Lease/LeaseLeases',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesResponse.FromString,
                )


class LeaseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LeaseGrant(self, request, context):
        """LeaseGrant creates a lease which expires if the server does not receive a keepAlive
        within a given time to live period. All keys attached to the lease will be expired and
        deleted if the lease expires. Each expired key generates a delete event in the event history.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaseRevoke(self, request, context):
        """LeaseRevoke revokes a lease. All keys attached to the lease will expire and be deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaseKeepAlive(self, request_iterator, context):
        """LeaseKeepAlive keeps the lease alive by streaming keep alive requests from the client
        to the server and streaming keep alive responses from the server to the client.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaseTimeToLive(self, request, context):
        """LeaseTimeToLive retrieves lease information.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaseLeases(self, request, context):
        """LeaseLeases lists all existing leases.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LeaseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LeaseGrant': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaseGrant,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantResponse.SerializeToString,
            ),
            'LeaseRevoke': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaseRevoke,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeResponse.SerializeToString,
            ),
            'LeaseKeepAlive': grpc.stream_stream_rpc_method_handler(
                    servicer.LeaseKeepAlive,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveResponse.SerializeToString,
            ),
            'LeaseTimeToLive': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaseTimeToLive,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveResponse.SerializeToString,
            ),
            'LeaseLeases': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaseLeases,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'etcdserverpb.Lease', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Lease(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LeaseGrant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.Lease/LeaseGrant',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseGrantResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaseRevoke(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.Lease/LeaseRevoke',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseRevokeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaseKeepAlive(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/etcdserverpb.Lease/LeaseKeepAlive',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseKeepAliveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaseTimeToLive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.Lease/LeaseTimeToLive',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseTimeToLiveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaseLeases(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.Lease/LeaseLeases',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.LeaseLeasesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Authenticate = channel.unary_unary(
                '/etcdserverpb.Auth/Authenticate',
                request_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateRequest.SerializeToString,
                response_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateResponse.FromString,
                )


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Authenticate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Authenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateRequest.FromString,
                    response_serializer=stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'etcdserverpb.Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Authenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/etcdserverpb.Auth/Authenticate',
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateRequest.SerializeToString,
            stormlock_dot_backends_dot_etcd_dot_proto_dot_rpc__pb2.AuthenticateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
