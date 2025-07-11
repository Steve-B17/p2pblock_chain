# EduCoin P2P Blockchain Simulation

A professional web-based simulation of a peer-to-peer blockchain network for educational purposes. Each node runs independently and syncs with peers, demonstrating mining, transactions, and consensus.

## Features
- Simple blockchain with proof-of-work
- Multiple nodes (run on different ports)
- Peer discovery and registration
- Longest-chain consensus
- Mining and transaction pool
- Modern Bootstrap UI dashboard

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running Multiple Nodes
You can run several nodes on different ports to simulate a network.

**Example:**
```sh
# Terminal 1
set PORT=5000 && python app.py
# Terminal 2
set PORT=5001 && python app.py
# Terminal 3
set PORT=5002 && python app.py
```

On Linux/Mac, use `export PORT=5001` instead of `set`.

## Using the Dashboard
1. Open each node in your browser:  
   - http://localhost:5000  
   - http://localhost:5001  
   - http://localhost:5002
2. Register peers (e.g., from 5000, add `localhost:5001` and `localhost:5002` as peers).
3. Add transactions, mine blocks, and sync chains using the dashboard buttons.
4. Use the "Sync/Resolve Chain" button to resolve conflicts and ensure all nodes have the longest chain.

## Screenshots/Logs
- Take screenshots of the dashboard showing synced chains and peer lists.
- Copy logs from the terminal to show mining and syncing actions.

## Customization
- You can adjust mining difficulty in `blockchain.py` (`Blockchain.difficulty`).
- The UI is built with Bootstrap and can be customized in `templates/index.html` and `static/style.css`.

## License
MIT 