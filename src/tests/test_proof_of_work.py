import unittest
from src.feature.proof_of_work import ProofOfWork

class TestProofOfWork(unittest.TestCase):
    def test_calculate_hash(self):
        proof_of_work = ProofOfWork(1, "previous_hash", ["transaction1", "transaction2"])
        self.assertEqual(len(proof_of_work.calculate_hash()), 64)

    def test_mine(self):
        proof_of_work = ProofOfWork(1, "previous_hash", ["transaction1", "transaction2"])
        self.assertTrue(proof_of_work.mine(4))

    def test_verify(self):
        proof_of_work = ProofOfWork(1, "previous_hash", ["transaction1", "transaction2"])
        proof_of_work.mine(4)
        self.assertTrue(proof_of_work.verify(4))

if __name__ == "__main__":
    unittest.main()