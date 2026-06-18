from typing import List
from src.models.block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self) -> Block:
        block_number = 0
        previous_hash = "0" * 64
        transactions = {"sender": "Genesis", "receiver": "Genesis", "amount": 0}
        nonce = 0
        hash = "0000000000000000000000000000000000000000000000000000000000000000"
        return Block(block_number, previous_hash, transactions, nonce, hash)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block) -> bool:
        if block.validate(self.difficulty):
            self.chain.append(block)
            return True
        return False

    def get_chain(self) -> List[Block]:
        return self.chain

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    block_number = 1
    previous_hash = blockchain.get_latest_block().get_hash()
    transactions = {"sender": "A", "receiver": "B", "amount": 10}
    nonce = 100
    hash = "0000000000000000000000000000000000000000000000000000000000000000"
    block = Block(block_number, previous_hash, transactions, nonce, hash)
    blockchain.add_block(block)
    print(f"Blockchain length: {len(blockchain.get_chain())}")