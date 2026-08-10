from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from src.feature.blockchain import Blockchain
from src.feature.p2p_networking import P2PNetworking
from src.feature.proof_of_work import ProofOfWork
from src.models.block import Block
from src.utils.cache import Cache

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    """
    API endpoint for healthcheck and node status.
    
    Returns:
    - A JSON response with the node's status, including the blockchain height, 
      the number of peers in the P2P network, and the current proof-of-work difficulty.
    """
    blockchain = Blockchain()
    p2p_networking = P2PNetworking()
    proof_of_work = ProofOfWork()
    
    # Get the current blockchain height
    blockchain_height = blockchain.get_height()
    
    # Get the number of peers in the P2P network
    num_peers = p2p_networking.get_num_peers()
    
    # Get the current proof-of-work difficulty
    difficulty = proof_of_work.get_difficulty()
    
    # Create a JSON response with the node's status
    response = {
        "status": "ok",
        "blockchain_height": blockchain_height,
        "num_peers": num_peers,
        "difficulty": difficulty
    }
    
    return JSONResponse(content=response, status_code=200)

@router.get("/node-status")
async def node_status():
    """
    API endpoint for detailed node status.
    
    Returns:
    - A JSON response with detailed information about the node, including the 
      blockchain height, the number of peers in the P2P network, the current 
      proof-of-work difficulty, and the last block in the blockchain.
    """
    blockchain = Blockchain()
    p2p_networking = P2PNetworking()
    proof_of_work = ProofOfWork()
    cache = Cache()
    
    # Get the current blockchain height
    blockchain_height = blockchain.get_height()
    
    # Get the number of peers in the P2P network
    num_peers = p2p_networking.get_num_peers()
    
    # Get the current proof-of-work difficulty
    difficulty = proof_of_work.get_difficulty()
    
    # Get the last block in the blockchain
    last_block = blockchain.get_last_block()
    
    # Create a JSON response with detailed information about the node
    response = {
        "status": "ok",
        "blockchain_height": blockchain_height,
        "num_peers": num_peers,
        "difficulty": difficulty,
        "last_block": {
            "hash": last_block.hash,
            "height": last_block.height,
            "timestamp": last_block.timestamp,
            "transactions": last_block.transactions
        }
    }
    
    # Cache the response for 1 minute
    cache.set("node_status", response, 60)
    
    return JSONResponse(content=response, status_code=200)

@router.get("/cache-status")
async def cache_status():
    """
    API endpoint for cache status.
    
    Returns:
    - A JSON response with information about the cache, including the number 
      of items in the cache and the cache hit ratio.
    """
    cache = Cache()
    
    # Get the number of items in the cache
    num_items = cache.get_num_items()
    
    # Get the cache hit ratio
    hit_ratio = cache.get_hit_ratio()
    
    # Create a JSON response with information about the cache
    response = {
        "status": "ok",
        "num_items": num_items,
        "hit_ratio": hit_ratio
    }
    
    return JSONResponse(content=response, status_code=200)