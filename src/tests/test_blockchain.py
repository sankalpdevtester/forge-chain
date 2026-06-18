import unittest
from src.feature.blockchain import Blockchain
from src.models.block import Block

class TestBlockchain(unittest.TestCase):
    def test_create_genesis_block(self):
        blockchain = Blockchain()
        genesis_block = blockchain.create_genesis_block()
        self.assertEqual(genesis_block.get_block_number(), 0)
        self.assertEqual(genesis_block.get_previous_hash(), "0" * 64)
        self.assertEqual(genesis_block.get_transactions(), {"sender": "Genesis", "receiver": "Genesis", "amount": 0})
        self.assertEqual(genesis_block.get_nonce(), 0)
        self.assertEqual(genesis_block.get_hash(), "0000000000000000000000000000000000000000000000000000000000000000")

    def test_add_block(self):
        blockchain = Blockchain()
        block_number = 1
        previous_hash = blockchain.get_latest_block().get_hash()
        transactions = {"sender": "A", "receiver": "B", "amount": 10}
        nonce = 100
        hash = "0000000000000000000000000000000000000000000000000000000000000000"
        block = Block(block_number, previous_hash, transactions, nonce, hash)
        self.assertTrue(blockchain.add_block(block))
        self.assertEqual(len(blockchain.get_chain()), 2)

    def test_get_chain(self):
        blockchain = Blockchain()
        block_number = 1
        previous_hash = blockchain.get_latest_block().get_hash()
        transactions = {"sender": "A", "receiver": "B", "amount": 10}
        nonce = 100
        hash = "0000000000000000000000000000000000000000000000000000000000000000"
        block = Block(block_number, previous_hash, transactions, nonce, hash)
        blockchain.add_block(block)
        self.assertEqual(len(blockchain.get_chain()), 2)

if __name__ == "__main__":
    unittest.main()