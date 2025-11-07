import hashlib, json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else '1',
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, student_id, action, metadata=None):
        self.current_transactions.append({
            'student_id': student_id,
            'action': action,
            'metadata': metadata or {},
            'timestamp': time(),
        })
        return self.last_block['index'] + 1 if self.chain else 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
