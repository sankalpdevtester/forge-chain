import hashlib
import time
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from src.utils.cache import Cache

class ProofOfWork:
    def __init__(self, block_number: int, previous_hash: str, transactions: list):
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data = str(self.block_number) + self.previous_hash + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty: int) -> bool:
        start_time = time.time()
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        print(f"Block mined in {end_time - start_time} seconds")
        return True

    def verify(self, difficulty: int) -> bool:
        return self.hash[:difficulty] == '0' * difficulty

    def get_hash(self) -> str:
        return self.hash

    def get_nonce(self) -> int:
        return self.nonce