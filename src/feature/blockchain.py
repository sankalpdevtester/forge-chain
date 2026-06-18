from typing import List
from src.models.block import Block
from src.feature.proof_of_work import ProofOfWork

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4  # adjust difficulty level as needed

    def create_genesis_block(self) -> Block:
        return Block(0, "0", ["Genesis transaction"])

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block) -> bool:
        if block.verify(self.difficulty):
            self.chain.append(block)
            return True
        else:
            return False

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.proof_of_work.get_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True