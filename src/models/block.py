from typing import Any, List
from pydantic import BaseModel
from src.feature.proof_of_work import ProofOfWork

class Block(BaseModel):
    block_number: int
    previous_hash: str
    transactions: List[Any]
    nonce: int
    hash: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, block_number: int, previous_hash: str, transactions: List[Any]):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof_of_work = ProofOfWork(block_number, previous_hash, transactions)
        self.nonce = self.proof_of_work.get_nonce()
        self.hash = self.proof_of_work.get_hash()

    def mine(self, difficulty: int) -> bool:
        return self.proof_of_work.mine(difficulty)

    def verify(self, difficulty: int) -> bool:
        return self.proof_of_work.verify(difficulty)