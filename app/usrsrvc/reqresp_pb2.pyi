from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
import dto_pb2 as _dto_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegistrationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGISTRATION_STATUS_UNSPECIFIED: _ClassVar[RegistrationStatus]
    REGISTRATION_STATUS_CREATED: _ClassVar[RegistrationStatus]
    REGISTRATION_STATUS_ALREADY_PRESENT: _ClassVar[RegistrationStatus]

class PremiumVariant(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PREMIUM_VARIANT_UNSPECIFIED: _ClassVar[PremiumVariant]
    PREMIUM_VARIANT_MONTH: _ClassVar[PremiumVariant]
    PREMIUM_VARIANT_QUARTER: _ClassVar[PremiumVariant]
    PREMIUM_VARIANT_HALF_YEAR: _ClassVar[PremiumVariant]
    PREMIUM_VARIANT_YEAR: _ClassVar[PremiumVariant]
REGISTRATION_STATUS_UNSPECIFIED: RegistrationStatus
REGISTRATION_STATUS_CREATED: RegistrationStatus
REGISTRATION_STATUS_ALREADY_PRESENT: RegistrationStatus
PREMIUM_VARIANT_UNSPECIFIED: PremiumVariant
PREMIUM_VARIANT_MONTH: PremiumVariant
PREMIUM_VARIANT_QUARTER: PremiumVariant
PREMIUM_VARIANT_HALF_YEAR: PremiumVariant
PREMIUM_VARIANT_YEAR: PremiumVariant

class GetUserRequest(_message.Message):
    __slots__ = ("id", "by_external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    BY_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    by_external_id: bool
    def __init__(self, id: _Optional[int] = ..., by_external_id: bool = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("id", "language", "location")
    ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    id: int
    language: str
    location: _dto_pb2.Location
    def __init__(self, id: _Optional[int] = ..., language: _Optional[str] = ..., location: _Optional[_Union[_dto_pb2.Location, _Mapping]] = ...) -> None: ...

class RegistrationRequest(_message.Message):
    __slots__ = ("user", "service", "consent_info")
    USER_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CONSENT_INFO_FIELD_NUMBER: _ClassVar[int]
    user: _dto_pb2.ExternalUser
    service: _dto_pb2.Service
    consent_info: _struct_pb2.Struct
    def __init__(self, user: _Optional[_Union[_dto_pb2.ExternalUser, _Mapping]] = ..., service: _Optional[_Union[_dto_pb2.Service, _Mapping]] = ..., consent_info: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RegistrationResponse(_message.Message):
    __slots__ = ("status", "id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    status: RegistrationStatus
    id: int
    def __init__(self, status: _Optional[_Union[RegistrationStatus, str]] = ..., id: _Optional[int] = ...) -> None: ...

class ActivatePremiumRequest(_message.Message):
    __slots__ = ("id", "variant")
    ID_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    id: int
    variant: PremiumVariant
    def __init__(self, id: _Optional[int] = ..., variant: _Optional[_Union[PremiumVariant, str]] = ...) -> None: ...

class ActivatePremiumResponse(_message.Message):
    __slots__ = ("updated", "active_till")
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TILL_FIELD_NUMBER: _ClassVar[int]
    updated: bool
    active_till: _timestamp_pb2.Timestamp
    def __init__(self, updated: bool = ..., active_till: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
