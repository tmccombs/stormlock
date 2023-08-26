#!/bin/sh

# Note, must be run from base directory of repository

PROTO_DIR=stormlock/backends/etcd/proto

python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. $PROTO_DIR/kv.proto $PROTO_DIR/rpc.proto
python3 -m grpc_tools.protoc --proto_path=. --grpc_python_out=. $PROTO_DIR/rpc.proto

# See https://github.com/protocolbuffers/protobuf/issues/11402
sed -i -E  -e 's/__slots__ = \[(.*)\]/__slots__ = (\1)/' $PROTO_DIR/*.pyi
