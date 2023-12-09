from pydantic import BaseModel

class ValidatorStateSnapshot(BaseModel):
    public_key: str
    index: str
    balance: str
    effective_balance: str
    state: str
    activation_epoch: str
    exit_epoch: str
    withdrawable_epoch: str
    slashed: bool