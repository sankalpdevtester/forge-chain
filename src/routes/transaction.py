from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.feature.blockchain import Blockchain
from src.feature.wallet import Wallet
from src.models.transaction import Transaction
from src.utils.cache import Cache

router = APIRouter()

class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: float

@router.post("/transactions")
async def create_transaction(transaction_request: TransactionRequest):
    """
    Create a new transaction and add it to the blockchain.
    """
    blockchain = Blockchain()
    wallet = Wallet()
    if not wallet.validate_address(transaction_request.sender):
        raise HTTPException(status_code=400, detail="Invalid sender address")
    if not wallet.validate_address(transaction_request.recipient):
        raise HTTPException(status_code=400, detail="Invalid recipient address")
    if transaction_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transaction amount")
    
    transaction = Transaction(
        sender=transaction_request.sender,
        recipient=transaction_request.recipient,
        amount=transaction_request.amount
    )
    blockchain.add_transaction(transaction)
    return JSONResponse(content={"message": "Transaction created successfully"}, status_code=201)

@router.get("/transactions")
async def get_transactions():
    """
    Retrieve all transactions from the blockchain.
    """
    blockchain = Blockchain()
    transactions = blockchain.get_transactions()
    return JSONResponse(content={"transactions": transactions}, status_code=200)

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    """
    Retrieve a specific transaction from the blockchain.
    """
    blockchain = Blockchain()
    transaction = blockchain.get_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return JSONResponse(content={"transaction": transaction}, status_code=200)

@router.get("/balance/{address}")
async def get_balance(address: str):
    """
    Retrieve the balance of a specific address.
    """
    blockchain = Blockchain()
    balance = blockchain.get_balance(address)
    return JSONResponse(content={"balance": balance}, status_code=200)

# Cache layer for API responses
cache = Cache()

@router.get("/transactions/cached")
async def get_transactions_cached():
    """
    Retrieve all transactions from the blockchain with caching.
    """
    cached_response = cache.get("transactions")
    if cached_response is not None:
        return JSONResponse(content=cached_response, status_code=200)
    transactions = blockchain.get_transactions()
    cache.set("transactions", transactions, 60)  # cache for 1 minute
    return JSONResponse(content={"transactions": transactions}, status_code=200)