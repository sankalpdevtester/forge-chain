"""Core blockchain implementation"""

import hashlib
import json
from time import time
from typing import List, Dict

class Blockchain:
    def __init__(self):
        self.chain: List[Dict] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = 4
        self.mining_reward = 50
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block"""
        genesis = {
            'index': 0,
            'timestamp': time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis['hash'] = self.calculate_hash(genesis)
        self.chain.append(genesis)
    
    def get_latest_block(self) -> Dict:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict) -> bool:
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address: str):
        """Mine all pending transactions"""
        # Reward miner
        reward = {'from': 'system', 'to': miner_address, 'amount': self.mining_reward}
        self.pending_transactions.append(reward)
        
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'previous_hash': self.get_latest_block()['hash'],
            'nonce': 0
        }
        
        # Proof of work
        block['nonce'], block['hash'] = self.proof_of_work(block)
        
        self.chain.append(block)
        self.pending_transactions = []
    
    def proof_of_work(self, block: Dict) -> tuple:
        """Find nonce that produces valid hash"""
        nonce = 0
        target = '0' * self.difficulty
        
        while True:
            block['nonce'] = nonce
            block_hash = self.calculate_hash(block)
            
            if block_hash[:self.difficulty] == target:
                return nonce, block_hash
            
            nonce += 1
    
    def calculate_hash(self, block: Dict) -> str:
        """Calculate SHA256 hash"""
        block_string = json.dumps({
            'index': block['index'],
            'timestamp': block['timestamp'],
            'transactions': block['transactions'],
            'previous_hash': block['previous_hash'],
            'nonce': block['nonce']
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def get_balance(self, address: str) -> float:
        """Calculate balance for address"""
        balance = 0
        
        for block in self.chain:
            for tx in block['transactions']:
                if tx['from'] == address:
                    balance -= tx['amount']
                if tx['to'] == address:
                    balance += tx['amount']
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """Validate blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Check hash
            if current['hash'] != self.calculate_hash(current):
                return False
            
            # Check chain link
            if current['previous_hash'] != previous['hash']:
                return False
        
        return True
