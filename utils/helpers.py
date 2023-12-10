from typing import Optional

from typing import List
from typing import Tuple
from web3 import Web3

from .models.data_models import ValidatorStateSnapshot
from .eth2 import BeaconNode

def safe_address_checksum(address: Optional[str]) -> Optional[str]:
    if address is None:
        return None
    return Web3.toChecksumAddress(address)

def getValidatorsSnapshots(validators) -> List[Tuple[str, ValidatorStateSnapshot]]:
    snapshots = []
    for key in validators:
        snapshots.append(
            (
                f"{key['index']}_{key['validator']['pubkey']}",
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
    return snapshots

# if __name__ == "__main__":
#     beacon = BeaconNode("https://cosmological-flashy-snow.ethereum-goerli.quiknode.pro/d969d3ab773d0b75252be64ea4b5d85e6634155f/")
#     validators = beacon.get_validators()
#     print(getValidatorsSnapshots(validators[-300:]))
