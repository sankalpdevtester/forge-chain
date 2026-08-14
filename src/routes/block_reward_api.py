from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.feature.blockchain import Blockchain
from src.feature.p2p_networking import P2PNetwork
from src.models.block import Block
from src.utils.cache import Cache

router = APIRouter()

class BlockRewardRequest(BaseModel):
    block_hash: str

class BlockRewardResponse(BaseModel):
    block_hash: str
    reward_amount: float
    reward_recipient: str

@router.post("/block_reward/distribute", response_model=BlockRewardResponse)
async def distribute_block_reward(block_reward_request: BlockRewardRequest):
    """
    Distribute block reward to the miner of the block.
    """
    blockchain = Blockchain()
    block = blockchain.get_block_by_hash(block_reward_request.block_hash)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    # Get the miner's wallet address from the block
    miner_address = block.miner

    # Calculate the block reward amount
    block_reward_amount = blockchain.calculate_block_reward(block.height)

    # Distribute the block reward to the miner's wallet
    p2p_network = P2PNetwork()
    p2p_network.distribute_block_reward(miner_address, block_reward_amount)

    # Return the block reward distribution result
    return BlockRewardResponse(
        block_hash=block_reward_request.block_hash,
        reward_amount=block_reward_amount,
        reward_recipient=miner_address
    )

@router.get("/block_reward/history", response_model=List[BlockRewardResponse])
async def get_block_reward_history():
    """
    Get the block reward distribution history.
    """
    cache = Cache()
    block_reward_history = cache.get("block_reward_history")
    if not block_reward_history:
        blockchain = Blockchain()
        block_reward_history = []
        for block in blockchain.get_all_blocks():
            block_reward_amount = blockchain.calculate_block_reward(block.height)
            block_reward_history.append(
                BlockRewardResponse(
                    block_hash=block.hash,
                    reward_amount=block_reward_amount,
                    reward_recipient=block.miner
                )
            )
        cache.set("block_reward_history", block_reward_history)
    return block_reward_history