"""REST API for blockchain"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
sys.path.append('..')

from src.blockchain import Blockchain

app = FastAPI(title="ForgeChain API")
blockchain = Blockchain()

class Transaction(BaseModel):
    from_address: str
    to_address: str
    amount: float

@app.get("/")
def root():
    return {"name": "ForgeChain API", "version": "1.0"}

@app.get("/chain")
def get_chain():
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }

@app.post("/transaction")
def add_transaction(tx: Transaction):
    blockchain.add_transaction(tx.dict())
    return {"message": "Transaction added"}

@app.post("/mine/{miner_address}")
def mine_block(miner_address: str):
    blockchain.mine_pending_transactions(miner_address)
    return {
        "message": "Block mined",
        "block": blockchain.get_latest_block()
    }

@app.get("/balance/{address}")
def get_balance(address: str):
    return {
        "address": address,
        "balance": blockchain.get_balance(address)
    }

@app.get("/validate")
def validate_chain():
    return {"valid": blockchain.is_chain_valid()}
