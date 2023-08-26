from stormlock.backends.etcd.proto import kv_pb2 as _kv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResponseHeader(_message.Message):
    __slots__ = ("cluster_id", "member_id", "revision", "raft_term")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    RAFT_TERM_FIELD_NUMBER: _ClassVar[int]
    cluster_id: int
    member_id: int
    revision: int
    raft_term: int
    def __init__(self, cluster_id: _Optional[int] = ..., member_id: _Optional[int] = ..., revision: _Optional[int] = ..., raft_term: _Optional[int] = ...) -> None: ...

class RangeRequest(_message.Message):
    __slots__ = ("key", "range_end", "limit", "revision", "sort_order", "sort_target", "serializable", "keys_only", "count_only", "min_mod_revision", "max_mod_revision", "min_create_revision", "max_create_revision")
    class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[RangeRequest.SortOrder]
        ASCEND: _ClassVar[RangeRequest.SortOrder]
        DESCEND: _ClassVar[RangeRequest.SortOrder]
    NONE: RangeRequest.SortOrder
    ASCEND: RangeRequest.SortOrder
    DESCEND: RangeRequest.SortOrder
    class SortTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        KEY: _ClassVar[RangeRequest.SortTarget]
        VERSION: _ClassVar[RangeRequest.SortTarget]
        CREATE: _ClassVar[RangeRequest.SortTarget]
        MOD: _ClassVar[RangeRequest.SortTarget]
        VALUE: _ClassVar[RangeRequest.SortTarget]
    KEY: RangeRequest.SortTarget
    VERSION: RangeRequest.SortTarget
    CREATE: RangeRequest.SortTarget
    MOD: RangeRequest.SortTarget
    VALUE: RangeRequest.SortTarget
    KEY_FIELD_NUMBER: _ClassVar[int]
    RANGE_END_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    SORT_TARGET_FIELD_NUMBER: _ClassVar[int]
    SERIALIZABLE_FIELD_NUMBER: _ClassVar[int]
    KEYS_ONLY_FIELD_NUMBER: _ClassVar[int]
    COUNT_ONLY_FIELD_NUMBER: _ClassVar[int]
    MIN_MOD_REVISION_FIELD_NUMBER: _ClassVar[int]
    MAX_MOD_REVISION_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATE_REVISION_FIELD_NUMBER: _ClassVar[int]
    MAX_CREATE_REVISION_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    range_end: bytes
    limit: int
    revision: int
    sort_order: RangeRequest.SortOrder
    sort_target: RangeRequest.SortTarget
    serializable: bool
    keys_only: bool
    count_only: bool
    min_mod_revision: int
    max_mod_revision: int
    min_create_revision: int
    max_create_revision: int
    def __init__(self, key: _Optional[bytes] = ..., range_end: _Optional[bytes] = ..., limit: _Optional[int] = ..., revision: _Optional[int] = ..., sort_order: _Optional[_Union[RangeRequest.SortOrder, str]] = ..., sort_target: _Optional[_Union[RangeRequest.SortTarget, str]] = ..., serializable: bool = ..., keys_only: bool = ..., count_only: bool = ..., min_mod_revision: _Optional[int] = ..., max_mod_revision: _Optional[int] = ..., min_create_revision: _Optional[int] = ..., max_create_revision: _Optional[int] = ...) -> None: ...

class RangeResponse(_message.Message):
    __slots__ = ("header", "kvs", "more", "count")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KVS_FIELD_NUMBER: _ClassVar[int]
    MORE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    kvs: _containers.RepeatedCompositeFieldContainer[_kv_pb2.KeyValue]
    more: bool
    count: int
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., kvs: _Optional[_Iterable[_Union[_kv_pb2.KeyValue, _Mapping]]] = ..., more: bool = ..., count: _Optional[int] = ...) -> None: ...

class PutRequest(_message.Message):
    __slots__ = ("key", "value", "lease", "prev_kv", "ignore_value", "ignore_lease")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    LEASE_FIELD_NUMBER: _ClassVar[int]
    PREV_KV_FIELD_NUMBER: _ClassVar[int]
    IGNORE_VALUE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_LEASE_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    value: bytes
    lease: int
    prev_kv: bool
    ignore_value: bool
    ignore_lease: bool
    def __init__(self, key: _Optional[bytes] = ..., value: _Optional[bytes] = ..., lease: _Optional[int] = ..., prev_kv: bool = ..., ignore_value: bool = ..., ignore_lease: bool = ...) -> None: ...

class PutResponse(_message.Message):
    __slots__ = ("header", "prev_kv")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PREV_KV_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    prev_kv: _kv_pb2.KeyValue
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., prev_kv: _Optional[_Union[_kv_pb2.KeyValue, _Mapping]] = ...) -> None: ...

class DeleteRangeRequest(_message.Message):
    __slots__ = ("key", "range_end", "prev_kv")
    KEY_FIELD_NUMBER: _ClassVar[int]
    RANGE_END_FIELD_NUMBER: _ClassVar[int]
    PREV_KV_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    range_end: bytes
    prev_kv: bool
    def __init__(self, key: _Optional[bytes] = ..., range_end: _Optional[bytes] = ..., prev_kv: bool = ...) -> None: ...

class DeleteRangeResponse(_message.Message):
    __slots__ = ("header", "deleted", "prev_kvs")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DELETED_FIELD_NUMBER: _ClassVar[int]
    PREV_KVS_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    deleted: int
    prev_kvs: _containers.RepeatedCompositeFieldContainer[_kv_pb2.KeyValue]
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., deleted: _Optional[int] = ..., prev_kvs: _Optional[_Iterable[_Union[_kv_pb2.KeyValue, _Mapping]]] = ...) -> None: ...

class RequestOp(_message.Message):
    __slots__ = ("request_range", "request_put", "request_delete_range", "request_txn")
    REQUEST_RANGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_PUT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DELETE_RANGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TXN_FIELD_NUMBER: _ClassVar[int]
    request_range: RangeRequest
    request_put: PutRequest
    request_delete_range: DeleteRangeRequest
    request_txn: TxnRequest
    def __init__(self, request_range: _Optional[_Union[RangeRequest, _Mapping]] = ..., request_put: _Optional[_Union[PutRequest, _Mapping]] = ..., request_delete_range: _Optional[_Union[DeleteRangeRequest, _Mapping]] = ..., request_txn: _Optional[_Union[TxnRequest, _Mapping]] = ...) -> None: ...

class ResponseOp(_message.Message):
    __slots__ = ("response_range", "response_put", "response_delete_range", "response_txn")
    RESPONSE_RANGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_PUT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DELETE_RANGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TXN_FIELD_NUMBER: _ClassVar[int]
    response_range: RangeResponse
    response_put: PutResponse
    response_delete_range: DeleteRangeResponse
    response_txn: TxnResponse
    def __init__(self, response_range: _Optional[_Union[RangeResponse, _Mapping]] = ..., response_put: _Optional[_Union[PutResponse, _Mapping]] = ..., response_delete_range: _Optional[_Union[DeleteRangeResponse, _Mapping]] = ..., response_txn: _Optional[_Union[TxnResponse, _Mapping]] = ...) -> None: ...

class Compare(_message.Message):
    __slots__ = ("result", "target", "key", "version", "create_revision", "mod_revision", "value", "lease", "range_end")
    class CompareResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EQUAL: _ClassVar[Compare.CompareResult]
        GREATER: _ClassVar[Compare.CompareResult]
        LESS: _ClassVar[Compare.CompareResult]
        NOT_EQUAL: _ClassVar[Compare.CompareResult]
    EQUAL: Compare.CompareResult
    GREATER: Compare.CompareResult
    LESS: Compare.CompareResult
    NOT_EQUAL: Compare.CompareResult
    class CompareTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VERSION: _ClassVar[Compare.CompareTarget]
        CREATE: _ClassVar[Compare.CompareTarget]
        MOD: _ClassVar[Compare.CompareTarget]
        VALUE: _ClassVar[Compare.CompareTarget]
        LEASE: _ClassVar[Compare.CompareTarget]
    VERSION: Compare.CompareTarget
    CREATE: Compare.CompareTarget
    MOD: Compare.CompareTarget
    VALUE: Compare.CompareTarget
    LEASE: Compare.CompareTarget
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATE_REVISION_FIELD_NUMBER: _ClassVar[int]
    MOD_REVISION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    LEASE_FIELD_NUMBER: _ClassVar[int]
    RANGE_END_FIELD_NUMBER: _ClassVar[int]
    result: Compare.CompareResult
    target: Compare.CompareTarget
    key: bytes
    version: int
    create_revision: int
    mod_revision: int
    value: bytes
    lease: int
    range_end: bytes
    def __init__(self, result: _Optional[_Union[Compare.CompareResult, str]] = ..., target: _Optional[_Union[Compare.CompareTarget, str]] = ..., key: _Optional[bytes] = ..., version: _Optional[int] = ..., create_revision: _Optional[int] = ..., mod_revision: _Optional[int] = ..., value: _Optional[bytes] = ..., lease: _Optional[int] = ..., range_end: _Optional[bytes] = ...) -> None: ...

class TxnRequest(_message.Message):
    __slots__ = ("compare", "success", "failure")
    COMPARE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    compare: _containers.RepeatedCompositeFieldContainer[Compare]
    success: _containers.RepeatedCompositeFieldContainer[RequestOp]
    failure: _containers.RepeatedCompositeFieldContainer[RequestOp]
    def __init__(self, compare: _Optional[_Iterable[_Union[Compare, _Mapping]]] = ..., success: _Optional[_Iterable[_Union[RequestOp, _Mapping]]] = ..., failure: _Optional[_Iterable[_Union[RequestOp, _Mapping]]] = ...) -> None: ...

class TxnResponse(_message.Message):
    __slots__ = ("header", "succeeded", "responses")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    succeeded: bool
    responses: _containers.RepeatedCompositeFieldContainer[ResponseOp]
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., succeeded: bool = ..., responses: _Optional[_Iterable[_Union[ResponseOp, _Mapping]]] = ...) -> None: ...

class CompactionRequest(_message.Message):
    __slots__ = ("revision", "physical")
    REVISION_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_FIELD_NUMBER: _ClassVar[int]
    revision: int
    physical: bool
    def __init__(self, revision: _Optional[int] = ..., physical: bool = ...) -> None: ...

class CompactionResponse(_message.Message):
    __slots__ = ("header")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ...) -> None: ...

class HashRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HashKVRequest(_message.Message):
    __slots__ = ("revision")
    REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: int
    def __init__(self, revision: _Optional[int] = ...) -> None: ...

class HashKVResponse(_message.Message):
    __slots__ = ("header", "hash", "compact_revision", "hash_revision")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    COMPACT_REVISION_FIELD_NUMBER: _ClassVar[int]
    HASH_REVISION_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    hash: int
    compact_revision: int
    hash_revision: int
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., hash: _Optional[int] = ..., compact_revision: _Optional[int] = ..., hash_revision: _Optional[int] = ...) -> None: ...

class HashResponse(_message.Message):
    __slots__ = ("header", "hash")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    hash: int
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., hash: _Optional[int] = ...) -> None: ...

class SnapshotRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SnapshotResponse(_message.Message):
    __slots__ = ("header", "remaining_bytes", "blob", "version")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REMAINING_BYTES_FIELD_NUMBER: _ClassVar[int]
    BLOB_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    remaining_bytes: int
    blob: bytes
    version: str
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., remaining_bytes: _Optional[int] = ..., blob: _Optional[bytes] = ..., version: _Optional[str] = ...) -> None: ...

class LeaseGrantRequest(_message.Message):
    __slots__ = ("TTL", "ID")
    TTL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TTL: int
    ID: int
    def __init__(self, TTL: _Optional[int] = ..., ID: _Optional[int] = ...) -> None: ...

class LeaseGrantResponse(_message.Message):
    __slots__ = ("header", "ID", "TTL", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    ID: int
    TTL: int
    error: str
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., ID: _Optional[int] = ..., TTL: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...

class LeaseRevokeRequest(_message.Message):
    __slots__ = ("ID")
    ID_FIELD_NUMBER: _ClassVar[int]
    ID: int
    def __init__(self, ID: _Optional[int] = ...) -> None: ...

class LeaseRevokeResponse(_message.Message):
    __slots__ = ("header")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ...) -> None: ...

class LeaseCheckpoint(_message.Message):
    __slots__ = ("ID", "remaining_TTL")
    ID_FIELD_NUMBER: _ClassVar[int]
    REMAINING_TTL_FIELD_NUMBER: _ClassVar[int]
    ID: int
    remaining_TTL: int
    def __init__(self, ID: _Optional[int] = ..., remaining_TTL: _Optional[int] = ...) -> None: ...

class LeaseCheckpointRequest(_message.Message):
    __slots__ = ("checkpoints")
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    checkpoints: _containers.RepeatedCompositeFieldContainer[LeaseCheckpoint]
    def __init__(self, checkpoints: _Optional[_Iterable[_Union[LeaseCheckpoint, _Mapping]]] = ...) -> None: ...

class LeaseCheckpointResponse(_message.Message):
    __slots__ = ("header")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ...) -> None: ...

class LeaseKeepAliveRequest(_message.Message):
    __slots__ = ("ID")
    ID_FIELD_NUMBER: _ClassVar[int]
    ID: int
    def __init__(self, ID: _Optional[int] = ...) -> None: ...

class LeaseKeepAliveResponse(_message.Message):
    __slots__ = ("header", "ID", "TTL")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    ID: int
    TTL: int
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., ID: _Optional[int] = ..., TTL: _Optional[int] = ...) -> None: ...

class LeaseTimeToLiveRequest(_message.Message):
    __slots__ = ("ID", "keys")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    ID: int
    keys: bool
    def __init__(self, ID: _Optional[int] = ..., keys: bool = ...) -> None: ...

class LeaseTimeToLiveResponse(_message.Message):
    __slots__ = ("header", "ID", "TTL", "grantedTTL", "keys")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    GRANTEDTTL_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    ID: int
    TTL: int
    grantedTTL: int
    keys: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., ID: _Optional[int] = ..., TTL: _Optional[int] = ..., grantedTTL: _Optional[int] = ..., keys: _Optional[_Iterable[bytes]] = ...) -> None: ...

class LeaseLeasesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LeaseStatus(_message.Message):
    __slots__ = ("ID")
    ID_FIELD_NUMBER: _ClassVar[int]
    ID: int
    def __init__(self, ID: _Optional[int] = ...) -> None: ...

class LeaseLeasesResponse(_message.Message):
    __slots__ = ("header", "leases")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LEASES_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    leases: _containers.RepeatedCompositeFieldContainer[LeaseStatus]
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., leases: _Optional[_Iterable[_Union[LeaseStatus, _Mapping]]] = ...) -> None: ...

class AuthenticateRequest(_message.Message):
    __slots__ = ("name", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    password: str
    def __init__(self, name: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class AuthenticateResponse(_message.Message):
    __slots__ = ("header", "token")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    header: ResponseHeader
    token: str
    def __init__(self, header: _Optional[_Union[ResponseHeader, _Mapping]] = ..., token: _Optional[str] = ...) -> None: ...
