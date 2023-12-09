import json
from typing import List
from typing import Tuple
from typing import Union

from redis import asyncio as aioredis

from .utils.event_log_decoder import EventLogDecoder
from .utils.models.message_models import TrackingWalletInteractionSnapshot
from snapshotter.utils.callback_helpers import GenericProcessorSnapshot
from snapshotter.utils.default_logger import logger
from snapshotter.utils.models.message_models import EthTransactionReceipt
from snapshotter.utils.models.message_models import PowerloomSnapshotProcessMessage
from snapshotter.utils.redis.redis_keys import epoch_txs_htable
from snapshotter.utils.rpc import RpcHelper


class TrackingWalletInteractionProcessor(GenericProcessorSnapshot):
    transformation_lambdas = None

    def __init__(self) -> None:
        self.transformation_lambdas = []
        self._logger = logger.bind(module='TrackingWalletInteractionProcessor')

    async def compute(
        self,
        epoch: PowerloomSnapshotProcessMessage,
        redis_conn: aioredis.Redis,
        rpc_helper: RpcHelper,

    ) -> Union[None, List[Tuple[str, TrackingWalletInteractionSnapshot]]]:
        min_chain_height = epoch.begin
        max_chain_height = epoch.end

        snapshots = (
                    f"{'0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13'}_{'0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13'}",
                    TrackingWalletInteractionSnapshot(
                        wallet_address='0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13',
                        contract_address='0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13',
                    ),
                )

        return [snapshots]
