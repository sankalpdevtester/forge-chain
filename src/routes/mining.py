from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from src.feature.proof_of_work import ProofOfWork
from src.models.block import Block

app = FastAPI()

class MiningRequest(BaseModel):
    block_number: int
    previous_hash: str
    transactions: Dict

@app.post("/mine")
async def mine(mining_request: MiningRequest):
    proof_of_work = ProofOfWork(mining_request.block_number, mining_request.previous_hash, mining_request.transactions)
    difficulty = 4
    start_time = time()
    proof_of_work.mine(difficulty)
    end_time = time()
    block = Block(proof_of_work.get_block_number(), proof_of_work.get_previous_hash(), proof_of_work.get_transactions(), proof_of_work.get_nonce(), proof_of_work.get_hash())
    return {
        "block_number": block.get_block_number(),
        "previous_hash": block.get_previous_hash(),
        "transactions": block.get_transactions(),
        "nonce": block.get_nonce(),
        "hash": block.get_hash(),
        "time": end_time - start_time
    }

# Example usage
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)