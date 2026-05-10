```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import time
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the blockchain
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_data = []

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block", self.calculate_hash(0, "0", int(time.time()), "Genesis Block"))

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return sha256(value.encode('utf-8')).hexdigest()

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = self.calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data)
        self.chain.append(new_block)

    def add_data(self, data):
        self.pending_data.append(data)

    def mine_pending_data(self):
        if not self.pending_data:
            return False

        new_block_index = len(self.chain)
        new_block_timestamp = int(time.time())
        new_block = Block(new_block_index, self.chain[-1].hash, new_block_timestamp, self.pending_data, self.calculate_hash(new_block_index, self.chain[-1].hash, new_block_timestamp, self.pending_data))
        self.add_block(new_block)
        self.pending_data = []
        return new_block

# Set up the wallet
class Wallet:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.address = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

    def sign_transaction(self, transaction):
        signature = self.private_key.sign(
            transaction.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

# Set up the app
app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the blockchain and wallet
blockchain = Blockchain()
wallet = Wallet()

# Define routes
@app.get("/blockchain")
async def get_blockchain():
    return JSONResponse(content={"blockchain": [block.__dict__ for block in blockchain.chain]}, media_type="application/json")

@app.post("/add_data")
async def add_data(data: str):
    blockchain.add_data(data)
    return JSONResponse(content={"message": "Data added to pending data"}, media_type="application/json")

@app.post("/mine_pending_data")
async def mine_pending_data():
    new_block = blockchain.mine_pending_data()
    if new_block:
        return JSONResponse(content={"message": "New block mined", "block": new_block.__dict__}, media_type="application/json")
    else:
        return JSONResponse(content={"message": "No pending data to mine"}, media_type="application/json")

@app.get("/wallet")
async def get_wallet():
    return JSONResponse(content={"address": wallet.address}, media_type="application/json")

@app.post("/sign_transaction")
async def sign_transaction(transaction: str):
    signature = wallet.sign_transaction(transaction)
    return JSONResponse(content={"signature": signature}, media_type="application/json")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```