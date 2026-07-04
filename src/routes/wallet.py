from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from src.models.block import Block
from src.feature.blockchain import Blockchain
from src.feature.wallet import Wallet
from src.utils.cache import Cache

router = APIRouter()

@router.post("/wallet/generate")
async def generate_wallet():
    """
    Generate a new ECDSA wallet and return the public and private keys.
    """
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    return {
        "private_key": private_pem.decode(),
        "public_key": public_pem.decode()
    }

@router.post("/wallet/import")
async def import_wallet(private_key: str):
    """
    Import an existing ECDSA wallet from a private key.
    """
    try:
        private_key_bytes = private_key.encode()
        private_key_loaded = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )
        public_key = private_key_loaded.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        return {
            "public_key": public_pem.decode()
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid private key")

@router.get("/wallet/balance/{address}")
async def get_balance(address: str, blockchain: Blockchain = Depends()):
    """
    Get the balance of a wallet address.
    """
    balance = blockchain.get_balance(address)
    return {
        "balance": balance
    }

@router.post("/wallet/transaction")
async def send_transaction(from_address: str, to_address: str, amount: int, private_key: str, blockchain: Blockchain = Depends()):
    """
    Send a transaction from one wallet address to another.
    """
    try:
        private_key_bytes = private_key.encode()
        private_key_loaded = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )
        wallet = Wallet(private_key_loaded, from_address)
        transaction = wallet.send_transaction(to_address, amount)
        blockchain.add_transaction(transaction)
        return {
            "transaction_id": transaction.id
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid private key or insufficient balance")