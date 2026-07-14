from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.models.block import Block
from src.models.transaction import Transaction
from src.utils.cache import Cache

class ValidationMiddleware:
    def __init__(self, app):
        self.app = app
        self.cache = Cache()

    async def __call__(self, request: Request):
        try:
            # Validate block creation request
            if request.url.path == "/mining/create_block":
                data = await request.json()
                Block.parse_obj(data)

            # Validate transaction creation request
            elif request.url.path == "/transaction/create":
                data = await request.json()
                Transaction.parse_obj(data)

            # Validate wallet creation request
            elif request.url.path == "/wallet/create":
                data = await request.json()
                # Assuming wallet model is defined in src/models/wallet.py
                from src.models.wallet import Wallet
                Wallet.parse_obj(data)

            # Call the next middleware or route handler
            return await self.app(request)

        except ValidationError as e:
            return JSONResponse(content={"error": "Invalid request data", "details": str(e)}, status_code=400)

        except Exception as e:
            return JSONResponse(content={"error": "Internal server error", "details": str(e)}, status_code=500)


def validate_blockchain_data(data: dict):
    """
    Validate blockchain data before adding it to the chain.
    """
    # Check if the data contains the required fields
    required_fields = ["block_number", "timestamp", "transactions", "previous_hash"]
    if not all(field in data for field in required_fields):
        raise ValueError("Invalid blockchain data")

    # Check if the transactions are valid
    for transaction in data["transactions"]:
        # Assuming transaction model is defined in src/models/transaction.py
        from src.models.transaction import Transaction
        try:
            Transaction.parse_obj(transaction)
        except ValidationError as e:
            raise ValueError("Invalid transaction data") from e

    return True


def validate_transaction_data(data: dict):
    """
    Validate transaction data before adding it to the blockchain.
    """
    # Check if the data contains the required fields
    required_fields = ["sender", "receiver", "amount"]
    if not all(field in data for field in required_fields):
        raise ValueError("Invalid transaction data")

    # Check if the sender and receiver are valid wallet addresses
    # Assuming wallet model is defined in src/models/wallet.py
    from src.models.wallet import Wallet
    try:
        Wallet.parse_obj({"address": data["sender"]})
        Wallet.parse_obj({"address": data["receiver"]})
    except ValidationError as e:
        raise ValueError("Invalid wallet address") from e

    return True