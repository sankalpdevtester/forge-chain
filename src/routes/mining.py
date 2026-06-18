from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.feature.proof_of_work import ProofOfWork
from src.models.block import Block

router = APIRouter()

class MiningRequest(BaseModel):
    block_number: int
    previous_hash: str
    transactions: list

@router.post("/mine")
async def mine_block(mining_request: MiningRequest):
    block = Block(mining_request.block_number, mining_request.previous_hash, mining_request.transactions)
    difficulty = 4  # adjust difficulty level as needed
    if block.mine(difficulty):
        return {"message": "Block mined successfully", "hash": block.hash}
    else:
        raise HTTPException(status_code=400, detail="Failed to mine block")

@router.get("/verify/{block_hash}")
async def verify_block(block_hash: str):
    # retrieve block from cache or database
    block = Block(1, "previous_hash", ["transaction1", "transaction2"])
    block.hash = block_hash
    difficulty = 4  # adjust difficulty level as needed
    if block.verify(difficulty):
        return {"message": "Block is valid"}
    else:
        raise HTTPException(status_code=400, detail="Block is invalid")