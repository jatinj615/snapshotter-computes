from typing import Optional

from typing import List
from typing import Tuple
from web3 import Web3

from .models.data_models import ValidatorStateSnapshot

def safe_address_checksum(address: Optional[str]) -> Optional[str]:
    if address is None:
        return None
    return Web3.toChecksumAddress(address)

def getValidatorsSnapshots(validators) -> List[Tuple[str, ValidatorStateSnapshot]]:
    snapshots = []
    for key in validators:
        snapshots.append(
            (
                f"{key['validator']['pubkey']}_{key['index']}",
                ValidatorStateSnapshot(
                    public_key = key["validator"]["pubkey"],
                    index = key["index"],
                    balance = key["balance"],
                    effective_balance = key["validator"]["effective_balance"],
                    state = key["status"],
                    activation_epoch = key["validator"]["activation_epoch"],
                    exit_epoch = key["validator"]["exit_epoch"],
                    withdrawable_epoch = key["validator"]["exit_epoch"],
                    slashed = key["validator"]["slashed"]
                )
            )
        )