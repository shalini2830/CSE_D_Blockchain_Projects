import hashlib
from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chain')
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/api/transactions/new', methods=['POST'])
def new_transaction():
    owner = request.form.get('owner')
    land_id = request.form.get('land_id')
    location = request.form.get('location')
    area = request.form.get('area')
    file = request.files.get('deed')
    file_bytes = file.read() if file else None

    if not owner or not land_id:
        return jsonify({'message': 'Missing required fields (owner, land_id)'}), 400

    doc_hash = hashlib.sha256(file_bytes).hexdigest() if file_bytes else None

    flagged = False
    flag_reason = None
    if doc_hash:
        for block in blockchain.chain:
            for tx in block['transactions']:
                if tx.get('doc_hash') == doc_hash:
                    flagged = True
                    flag_reason = 'Exact document hash already exists (duplicate)'

    index = blockchain.new_transaction(owner, land_id, location, area, doc_hash=doc_hash, flagged=flagged, flag_reason=flag_reason)
    return jsonify({'message': f'Transaction will be added to Block {index}', 'flagged': flagged, 'flag_reason': flag_reason}), 201

@app.route('/api/mine')
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    return jsonify({'message': 'New Block Forged', 'index': block['index'], 'transactions': block['transactions'], 'proof': block['proof'], 'previous_hash': block['previous_hash']}), 200

if __name__ == '__main__':
    app.run(debug=True)
