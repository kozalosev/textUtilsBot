import cachetools
import asyncache
import grpc
from typing import Optional
from .service_pb2_grpc import UserServiceStub
from .reqresp_pb2 import GetUserRequest
from data import config

# To regenerate gRPC classes:
#   pip install -r requirements-dev.txt
#   git submodule update --remote
#
#   cd app/usrsrvc
#   python -m grpc_tools.protoc -I../../user-service-proto --python_out=. --pyi_out=. --grpc_python_out=. ../../user-service-proto/*.proto


class Client:
    def __init__(self, addr: str):
        self._addr = addr
        self._inner: Optional[UserServiceStub] = None

    @asyncache.cached(cachetools.TTLCache(config.USER_SERVICE_CACHE_MAX_SIZE, config.USER_SERVICE_CACHE_TIME))
    async def get_lang_code(self, uid: int, default: Optional[str]) -> Optional[str]:
        req = GetUserRequest(id=uid, by_external_id=True)
        user = await self._client().get(req)
        return user.options.language_code or default

    def _client(self) -> UserServiceStub:
        if self._inner is None:
            channel = grpc.aio.insecure_channel(self._addr)
            self._inner = UserServiceStub(channel)
        return self._inner
