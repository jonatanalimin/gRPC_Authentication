# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\"\x1a\n\nsayRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\x0bsayResponse\x12\r\n\x05reply\x18\x01 \x01(\t2\x84\x01\n\x07Service\x12(\n\tsayPublic\x12\x0b.sayRequest\x1a\x0c.sayResponse\"\x00\x12&\n\x07sayUser\x12\x0b.sayRequest\x1a\x0c.sayResponse\"\x00\x12\'\n\x08sayAdmin\x12\x0b.sayRequest\x1a\x0c.sayResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SAYREQUEST._serialized_start=17
  _SAYREQUEST._serialized_end=43
  _SAYRESPONSE._serialized_start=45
  _SAYRESPONSE._serialized_end=73
  _SERVICE._serialized_start=76
  _SERVICE._serialized_end=208
# @@protoc_insertion_point(module_scope)