# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stormlock/backends/etcd/proto/kv.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&stormlock/backends/etcd/proto/kv.proto\x12\x06mvccpb\"u\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x17\n\x0f\x63reate_revision\x18\x02 \x01(\x03\x12\x14\n\x0cmod_revision\x18\x03 \x01(\x03\x12\x0f\n\x07version\x18\x04 \x01(\x03\x12\r\n\x05value\x18\x05 \x01(\x0c\x12\r\n\x05lease\x18\x06 \x01(\x03\"\x91\x01\n\x05\x45vent\x12%\n\x04type\x18\x01 \x01(\x0e\x32\x17.mvccpb.Event.EventType\x12\x1c\n\x02kv\x18\x02 \x01(\x0b\x32\x10.mvccpb.KeyValue\x12!\n\x07prev_kv\x18\x03 \x01(\x0b\x32\x10.mvccpb.KeyValue\" \n\tEventType\x12\x07\n\x03PUT\x10\x00\x12\n\n\x06\x44\x45LETE\x10\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stormlock.backends.etcd.proto.kv_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_KEYVALUE']._serialized_start=50
  _globals['_KEYVALUE']._serialized_end=167
  _globals['_EVENT']._serialized_start=170
  _globals['_EVENT']._serialized_end=315
  _globals['_EVENT_EVENTTYPE']._serialized_start=283
  _globals['_EVENT_EVENTTYPE']._serialized_end=315
# @@protoc_insertion_point(module_scope)
