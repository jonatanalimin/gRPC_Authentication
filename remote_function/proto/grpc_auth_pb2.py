# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_auth.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fgrpc_auth.proto\"2\n\x0cloginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"<\n\rloginResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x15\n\rrefresh_token\x18\x02 \x01(\t\"\'\n\x0erefreshRequest\x12\x15\n\rrefresh_token\x18\x01 \x01(\t\"\'\n\x0frefreshResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t2p\n\x0b\x41uthService\x12(\n\x05login\x12\r.loginRequest\x1a\x0e.loginResponse\"\x00\x12\x37\n\x10refreshing_token\x12\x0f.refreshRequest\x1a\x10.refreshResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_auth_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGINREQUEST._serialized_start=19
  _LOGINREQUEST._serialized_end=69
  _LOGINRESPONSE._serialized_start=71
  _LOGINRESPONSE._serialized_end=131
  _REFRESHREQUEST._serialized_start=133
  _REFRESHREQUEST._serialized_end=172
  _REFRESHRESPONSE._serialized_start=174
  _REFRESHRESPONSE._serialized_end=213
  _AUTHSERVICE._serialized_start=215
  _AUTHSERVICE._serialized_end=327
# @@protoc_insertion_point(module_scope)
