import asyncio
import cachetools
import asyncache
import grpc
import logging

from typing import Optional

from .service_pb2_grpc import UserServiceStub
from .reqresp_pb2 import GetUserRequest
from .. import config

# To regenerate gRPC classes:
#   pip install -r requirements-dev.txt
#   git submodule update --remote
#
#   cd app/usrsrvc
#   python -m grpc_tools.protoc -I../../user-service-proto --python_out=. --pyi_out=. --grpc_python_out=. ../../user-service-proto/*.proto


class Client:
    def __init__(self, addr: Optional[str]):
        if not addr:
            logging.warning("GRPC_ADDR_USER_SERVICE is not set; user-service integration is disabled")
        self._addr = addr
        self._inner: Optional[UserServiceStub] = None

    async def connect(self) -> None:
        if not self._addr:
            return
        channel = grpc.aio.insecure_channel(self._addr)
        try:
            await asyncio.wait_for(channel.channel_ready(), timeout=5.0)
            self._inner = UserServiceStub(channel)
        except (asyncio.TimeoutError, grpc.aio.AioRpcError) as e:
            logging.warning("user-service is unreachable (%s); integration disabled", e)
            await channel.close()

    @asyncache.cached(cachetools.TTLCache(config.USER_SERVICE_CACHE_MAX_SIZE, config.USER_SERVICE_CACHE_TIME))
    async def get_lang_code(self, uid: int, default: Optional[str]) -> str:
        if self._inner is None:
            return default or ""
        try:
            req = GetUserRequest(id=uid, by_external_id=True)
            user = await self._inner.get(req)
            return user.options.language_code or default or ""
        except grpc.aio.AioRpcError as e:
            logging.warning("user-service call failed (%s); falling back", e.details())
            return default or ""
