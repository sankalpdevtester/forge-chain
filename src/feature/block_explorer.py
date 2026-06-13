from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.feature.p2p_networking import get_blockchain
from src.utils.cache import Cache
from typing import List, Dict

router = APIRouter()

# Initialize cache with 1-hour TTL
cache = Cache(ttl=3600)

@router.get("/blocks/{block_height}", response_class=JSONResponse)
async def get_block(block_height: int):
    """
    Get block data by height.

    Args:
    block_height (int): The height of the block.

    Returns:
    JSONResponse: The block data.
    """
    blockchain = get_blockchain()
    if block_height < 0 or block_height >= len(blockchain):
        raise HTTPException(status_code=404, detail="Block not found")

    block = blockchain[block_height]
    return block

@router.get("/blocks", response_class=JSONResponse)
async def get_blocks():
    """
    Get all block data.

    Returns:
    JSONResponse: The list of block data.
    """
    blockchain = get_blockchain()
    return blockchain

@router.get("/block/height", response_class=JSONResponse)
async def get_block_height():
    """
    Get the current block height.

    Returns:
    JSONResponse: The current block height.
    """
    blockchain = get_blockchain()
    return {"height": len(blockchain)}

@router.get("/transaction/{tx_hash}", response_class=JSONResponse)
async def get_transaction(tx_hash: str):
    """
    Get transaction data by hash.

    Args:
    tx_hash (str): The hash of the transaction.

    Returns:
    JSONResponse: The transaction data.
    """
    blockchain = get_blockchain()
    for block in blockchain:
        for tx in block["transactions"]:
            if tx["hash"] == tx_hash:
                return tx

    raise HTTPException(status_code=404, detail="Transaction not found")

@router.get("/transactions", response_class=JSONResponse)
async def get_transactions():
    """
    Get all transaction data.

    Returns:
    JSONResponse: The list of transaction data.
    """
    blockchain = get_blockchain()
    transactions = []
    for block in blockchain:
        transactions.extend(block["transactions"])
    return transactions

# Cache block explorer data
@router.get("/block_explorer", response_class=JSONResponse)
async def get_block_explorer():
    """
    Get block explorer data.

    Returns:
    JSONResponse: The block explorer data.
    """
    cache_key = "block_explorer"
    if cache.exists(cache_key):
        return cache.get(cache_key)

    blockchain = get_blockchain()
    block_explorer_data = {
        "blocks": len(blockchain),
        "transactions": 0,
        "latest_block": blockchain[-1] if blockchain else None
    }
    for block in blockchain:
        block_explorer_data["transactions"] += len(block["transactions"])

    cache.set(cache_key, block_explorer_data)
    return block_explorer_data