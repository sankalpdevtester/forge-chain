from fastapi import FastAPI, WebSocket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from typing import List
import asyncio
import json
import logging

# Initialize the FastAPI app
app = FastAPI()

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the P2P networking class
class P2PNetwork:
    def __init__(self, node_id: str, node_address: str):
        self.node_id = node_id
        self.node_address = node_address
        self.peers = []

    # Add a new peer to the network
    async def add_peer(self, peer_id: str, peer_address: str):
        self.peers.append((peer_id, peer_address))
        logger.info(f"Added peer {peer_id} with address {peer_address}")

    # Remove a peer from the network
    async def remove_peer(self, peer_id: str):
        self.peers = [(pid, addr) for pid, addr in self.peers if pid != peer_id]
        logger.info(f"Removed peer {peer_id}")

    # Propagate a transaction to all peers
    async def propagate_transaction(self, transaction: dict):
        for peer_id, peer_address in self.peers:
            async with WebSocket(peer_address) as ws:
                await ws.send_json(transaction)
                logger.info(f"Propagated transaction to peer {peer_id}")

# Define the WebSocket endpoint for peer communication
@app.websocket("/p2p")
async def p2p_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_json()
            if message["type"] == "transaction":
                # Propagate the transaction to all peers
                p2p_network = P2PNetwork("node1", "ws://localhost:8000/p2p")
                await p2p_network.propagate_transaction(message["transaction"])
            elif message["type"] == "peer":
                # Add or remove a peer from the network
                if message["action"] == "add":
                    await p2p_network.add_peer(message["peer_id"], message["peer_address"])
                elif message["action"] == "remove":
                    await p2p_network.remove_peer(message["peer_id"])
        except Exception as e:
            logger.error(f"Error occurred: {e}")

# Generate a new ECDSA key pair for node authentication
def generate_ecdsa_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

# Initialize the P2P network with a new ECDSA key pair
p2p_network = P2PNetwork("node1", "ws://localhost:8000/p2p")
private_pem, public_pem = generate_ecdsa_key_pair()
logger.info(f"Initialized P2P network with node ID {p2p_network.node_id} and public key {public_pem.decode()}")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)