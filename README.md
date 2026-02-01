# ForgeChain - Blockchain Implementation

A complete blockchain implementation in Python with proof-of-work consensus, ECDSA signatures, and REST API.

## Features

- ⛏️ Proof-of-Work mining
- 🔐 ECDSA cryptographic signatures
- 💰 Wallet system
- 🌐 REST API
- ✅ Chain validation
- 🧪 Test coverage

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Start API server
```bash
uvicorn api.main:app --reload
```

### Create wallet
```bash
curl -X POST http://localhost:8000/wallet/create
```

### Mine block
```bash
curl -X POST http://localhost:8000/mine/your_address
```

## API Endpoints

- `GET /chain` - View blockchain
- `POST /transaction` - Add transaction
- `POST /mine/{address}` - Mine block
- `GET /balance/{address}` - Check balance
- `POST /wallet/create` - Create wallet

## Project Structure

```
├── src/
│   ├── blockchain.py    # Core blockchain
│   ├── block.py         # Block class
│   ├── transaction.py   # Transaction handling
│   ├── wallet.py        # Wallet & crypto
│   └── proof_of_work.py # Mining algorithm
├── api/
│   └── main.py          # REST API
└── tests/
    └── test_blockchain.py
```

## License

MIT
