from typing import Dict
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from src.feature.proof_of_work import ProofOfWork

class Block(BaseModel):
    block_number: int
    previous_hash: str
    transactions: Dict
    nonce: int
    hash: str

    def __init__(self, block_number: int, previous_hash: str, transactions: Dict, nonce: int, hash: str):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash

    def validate(self, difficulty: int) -> bool:
        proof_of_work = ProofOfWork(self.block_number, self.previous_hash, self.transactions)
        proof_of_work.nonce = self.nonce
        proof_of_work.hash = self.hash
        return proof_of_work.validate(difficulty)

    def get_block_number(self) -> int:
        return self.block_number

    def get_previous_hash(self) -> str:
        return self.previous_hash

    def get_transactions(self) -> Dict:
        return self.transactions

    def get_nonce(self) -> int:
        return self.nonce

    def get_hash(self) -> str:
        return self.hash

# Example usage
if __name__ == "__main__":
    block_number = 1
    previous_hash = "0" * 64
    transactions = {"sender": "A", "receiver": "B", "amount": 10}
    nonce = 100
    hash = "0000000000000000000000000000000000000000000000000000000000000000"
    block = Block(block_number, previous_hash, transactions, nonce, hash)
    difficulty = 4
    print(f"Block {block_number} is valid: {block.validate(difficulty)}")