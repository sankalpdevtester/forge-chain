# ForgeChain - Blockchain from Scratch
[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI Version](https://img.shields.io/badge/FastAPI-0.92.0+-green.svg)](https://fastapi.tiangolo.com/)
[![Cryptography Version](https://img.shields.io/badge/Cryptography-4.0.0+-yellow.svg)](https://cryptography.io/en/latest/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Description
ForgeChain is a fully functional blockchain implementation from scratch, built using Python, FastAPI, and cryptography. It features proof-of-work consensus, ECDSA wallet cryptography, a smart contract virtual machine, and a REST API for interaction. This project aims to provide a comprehensive and modular blockchain framework for developers and researchers.

## Features
* **Proof-of-Work Consensus**: A robust consensus algorithm ensuring the integrity of the blockchain
* **ECDSA Wallet Cryptography**: Secure wallet management using Elliptic Curve Digital Signature Algorithm
* **Smart Contract Virtual Machine**: Execute custom smart contracts on the blockchain
* **REST API**: Interact with the blockchain using a simple and intuitive API
* **Modular Architecture**: Easily extend or modify the blockchain framework to suit your needs

## Installation
To install ForgeChain, follow these steps:
1. **Clone the repository**: `git clone https://github.com/your-username/forgechain.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Initialize the blockchain**: `python init_blockchain.py`
4. **Start the API**: `uvicorn main:app --host 0.0.0.0 --port 8000`

## Usage
Interact with the blockchain using the REST API:
* **Get blockchain info**: `GET /blockchain/info`
* **Create a new wallet**: `POST /wallet/create`
* **Send a transaction**: `POST /transaction/send`
* **Execute a smart contract**: `POST /contract/execute`

## Architecture Overview
ForgeChain consists of the following components:
* **Blockchain**: The core blockchain framework, responsible for managing the chain of blocks
* **Wallet**: Secure wallet management using ECDSA cryptography
* **Smart Contract VM**: Executes custom smart contracts on the blockchain
* **REST API**: Provides a simple and intuitive interface for interacting with the blockchain

## Contributing
Contributions are welcome and encouraged. To contribute to ForgeChain, please:
1. **Fork the repository**: Create a fork of the ForgeChain repository
2. **Create a new branch**: Create a new branch for your feature or bug fix
3. **Submit a pull request**: Submit a pull request with your changes
4. **Review and merge**: Your changes will be reviewed and merged into the main branch

## License
ForgeChain is licensed under the Apache 2.0 license. See [LICENSE](LICENSE) for details.