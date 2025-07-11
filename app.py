from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
from blockchain import Blockchain, Block
import json
import os

app = Flask(__name__)
blockchain = Blockchain()

# Get port from environment or default
PORT = int(os.environ.get('PORT', 5000))

@app.route('/')
def index():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'transactions': block.transactions,
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': getattr(block, 'hash', block.compute_hash())
        })
    return render_template('index.html',
                           chain=chain_data,
                           peers=list(blockchain.peers),
                           unconfirmed=blockchain.unconfirmed_transactions,
                           port=PORT)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    recipient = request.form['recipient']
    amount = request.form['amount']
    if not sender or not recipient or not amount:
        return redirect(url_for('index', msg='Invalid transaction data.', type='error'))
    tx = {'sender': sender, 'recipient': recipient, 'amount': amount}
    blockchain.add_new_transaction(tx)
    return redirect(url_for('index', msg='Transaction added!', type='success'))

@app.route('/mine', methods=['POST'])
def mine():
    result = blockchain.mine()
    if not result:
        msg = 'No transactions to mine.'
        t = 'info'
    else:
        msg = f'Block #{result} is mined.'
        t = 'success'
    return redirect(url_for('index', msg=msg, type=t))

@app.route('/register_node', methods=['POST'])
def register_node():
    peer = request.form['peer']
    if not peer:
        return redirect(url_for('index', msg='Invalid peer address.', type='error'))
    blockchain.add_peer(peer)
    return redirect(url_for('index', msg='Peer added!', type='success'))

@app.route('/sync', methods=['POST'])
def sync():
    replaced = False
    for peer in blockchain.peers:
        try:
            url = f'http://{peer}/chain_json'
            resp = requests.get(url)
            if resp.status_code == 200:
                peer_chain = resp.json()['chain']
                peer_blocks = [Block(**block) for block in peer_chain]
                if blockchain.replace_chain(peer_blocks):
                    replaced = True
        except Exception:
            continue
    msg = 'Chain was replaced.' if replaced else 'No replacement needed.'
    t = 'success' if replaced else 'info'
    return redirect(url_for('index', msg=msg, type=t))

@app.route('/chain_json')
def chain_json():
    chain_data = []
    for block in blockchain.chain:
        block_data = block.__dict__.copy()
        block_data['hash'] = getattr(block, 'hash', block.compute_hash())
        chain_data.append(block_data)
    return jsonify({'length': len(chain_data), 'chain': chain_data})

@app.route('/peers')
def get_peers():
    return jsonify({'peers': list(blockchain.peers)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True) 