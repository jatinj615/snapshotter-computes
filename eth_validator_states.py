import json
from typing import List
from typing import Tuple
from typing import Union

from redis import asyncio as aioredis

from .utils.eth2 import BeaconNode
from .utils.models.data_models import ValidatorStateSnapshot
from snapshotter.utils.callback_helpers import GenericProcessorSnapshot
from snapshotter.utils.default_logger import logger
from .utils.helpers import getValidatorsSnapshots
from snapshotter.utils.models.message_models import PowerloomSnapshotProcessMessage
from snapshotter.utils.rpc import RpcHelper
from snapshotter.settings.config import settings


class ValidatorStateProcessor(GenericProcessorSnapshot):
    transformation_lambdas = None

    def __init__(self) -> None:
        self.transformation_lambdas = []
        self._logger = logger.bind(module='ValidatorStateProcessor')

    async def compute(
        self,
        epoch: PowerloomSnapshotProcessMessage,
        redis_conn: aioredis.Redis,
        rpc_helper: RpcHelper,

    ) -> Union[None, List[Tuple[str, ValidatorStateSnapshot]]]:
        beacon = BeaconNode(settings.rpc)
        validators = beacon.get_validators()
        return getValidatorsSnapshots(validators[-300:])
