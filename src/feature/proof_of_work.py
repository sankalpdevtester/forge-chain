from hashlib import sha256
from time import time
from typing import Dict

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from src.utils.cache import Cache

class ProofOfWork:
    def __init__(self, block_number: int, previous_hash: str, transactions: Dict):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data = str(self.block_number) + self.previous_hash + str(self.transactions) + str(self.nonce)
        return sha256(data.encode()).hexdigest()

    def mine(self, difficulty: int) -> bool:
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return True

    def validate(self, difficulty: int) -> bool:
        return self.hash[:difficulty] == '0' * difficulty

    def get_hash(self) -> str:
        return self.hash

    def get_nonce(self) -> int:
        return self.nonce

    def get_block_number(self) -> int:
        return self.block_number

    def get_previous_hash(self) -> str:
        return self.previous_hash

    def get_transactions(self) -> Dict:
        return self.transactions

# Example usage
if __name__ == "__main__":
    cache = Cache()
    block_number = 1
    previous_hash = "0" * 64
    transactions = {"sender": "A", "receiver": "B", "amount": 10}
    proof_of_work = ProofOfWork(block_number, previous_hash, transactions)
    difficulty = 4
    start_time = time()
    proof_of_work.mine(difficulty)
    end_time = time()
    print(f"Block {block_number} mined in {end_time - start_time} seconds")
    print(f"Hash: {proof_of_work.get_hash()}")
    print(f"Nonce: {proof_of_work.get_nonce()}")