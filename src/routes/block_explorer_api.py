from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from src.feature.blockchain import Blockchain
from src.feature.block_explorer import BlockExplorer
from src.models.block import Block

router = APIRouter()

class BlockExplorerRequest(BaseModel):
    block_hash: str = None
    block_height: int = None

@router.get("/blocks/{block_height}", response_class=JSONResponse)
async def get_block_by_height(block_height: int):
    """
    Get a block by its height.

    Args:
    block_height (int): The height of the block.

    Returns:
    JSONResponse: A JSON response containing the block data.
    """
    blockchain = Blockchain()
    block = blockchain.get_block_by_height(block_height)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    return block.to_dict()

@router.get("/blocks/hash/{block_hash}", response_class=JSONResponse)
async def get_block_by_hash(block_hash: str):
    """
    Get a block by its hash.

    Args:
    block_hash (str): The hash of the block.

    Returns:
    JSONResponse: A JSON response containing the block data.
    """
    blockchain = Blockchain()
    block = blockchain.get_block_by_hash(block_hash)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    return block.to_dict()

@router.get("/blocks", response_class=JSONResponse)
async def get_blocks():
    """
    Get a list of all blocks in the blockchain.

    Returns:
    JSONResponse: A JSON response containing a list of block data.
    """
    blockchain = Blockchain()
    blocks = blockchain.get_blocks()
    return [block.to_dict() for block in blocks]

@router.get("/block-explorer", response_class=JSONResponse)
async def get_block_explorer():
    """
    Get the block explorer data.

    Returns:
    JSONResponse: A JSON response containing the block explorer data.
    """
    block_explorer = BlockExplorer()
    return block_explorer.get_block_explorer_data()

@router.post("/block-explorer/search", response_class=JSONResponse)
async def search_block_explorer(request: BlockExplorerRequest):
    """
    Search the block explorer.

    Args:
    request (BlockExplorerRequest): A request containing the search parameters.

    Returns:
    JSONResponse: A JSON response containing the search results.
    """
    block_explorer = BlockExplorer()
    if request.block_hash:
        return block_explorer.search_by_hash(request.block_hash)
    elif request.block_height:
        return block_explorer.search_by_height(request.block_height)
    else:
        raise HTTPException(status_code=400, detail="Invalid search parameters")