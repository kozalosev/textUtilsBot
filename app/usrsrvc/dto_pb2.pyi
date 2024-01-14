from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVICE_TYPE_UNSPECIFIED: _ClassVar[ServiceType]
    SERVICE_TYPE_TELEGRAM_BOT: _ClassVar[ServiceType]
    SERVICE_TYPE_TELEGRAM_CHANNEL: _ClassVar[ServiceType]
    SERVICE_TYPE_WEBSITE: _ClassVar[ServiceType]
    SERVICE_TYPE_APPLICATION: _ClassVar[ServiceType]
SERVICE_TYPE_UNSPECIFIED: ServiceType
SERVICE_TYPE_TELEGRAM_BOT: ServiceType
SERVICE_TYPE_TELEGRAM_CHANNEL: ServiceType
SERVICE_TYPE_WEBSITE: ServiceType
SERVICE_TYPE_APPLICATION: ServiceType

class ExternalUser(_message.Message):
    __slots__ = ("external_id", "name")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    external_id: int
    name: str
    def __init__(self, external_id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "options", "is_premium")
    class Options(_message.Message):
        __slots__ = ("language_code", "location")
        LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        language_code: str
        location: Location
        def __init__(self, language_code: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IS_PREMIUM_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    options: User.Options
    is_premium: bool
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., options: _Optional[_Union[User.Options, _Mapping]] = ..., is_premium: bool = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class Service(_message.Message):
    __slots__ = ("name", "kind")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: ServiceType
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[_Union[ServiceType, str]] = ...) -> None: ...
