import hashlib
import json
from typing import List
from django.utils import timezone

from .models import Block


def hash_block_dict(block_dict: dict) -> str:
    block_string = json.dumps(block_dict, sort_keys=True).encode('utf-8')
    return hashlib.sha256(block_string).hexdigest()


def get_previous_block() -> Block | None:
    return Block.objects.order_by('-index').first()


def create_block(proof: int, previous_hash: str, certificate_hash: str, issuer: str) -> Block:
    new_index = 1
    previous_block = get_previous_block()
    if previous_block:
        new_index = previous_block.index + 1

    block_dict = {
        'index': new_index,
        'timestamp': timezone.now().isoformat(),
        'certificate_hash': certificate_hash,
        'previous_hash': previous_hash,
        'nonce': proof,
        'issuer': issuer,
    }

    block = Block.objects.create(
        index=new_index,
        certificate_hash=certificate_hash,
        previous_hash=previous_hash,
        nonce=proof,
        issuer=issuer,
    )
    return block


def hash_block(block: Block) -> str:
    block_dict = {
        'index': block.index,
        'timestamp': block.timestamp.isoformat(),
        'certificate_hash': block.certificate_hash,
        'previous_hash': block.previous_hash,
        'nonce': block.nonce,
        'issuer': block.issuer,
    }
    return hash_block_dict(block_dict)


def proof_of_work(previous_proof: int) -> int:
    new_proof = 1
    while True:
        check = hashlib.sha256(f"{new_proof**2 - previous_proof**2}".encode('utf-8')).hexdigest()
        if check.startswith('0000'):
            return new_proof
        new_proof += 1


def is_chain_valid(chain: List[Block]) -> bool:
    if not chain:
        return True
    for i in range(1, len(chain)):
        prev = chain[i - 1]
        curr = chain[i]
        if curr.previous_hash != hash_block(prev):
            return False
        check = hashlib.sha256(f"{curr.nonce**2 - prev.nonce**2}".encode('utf-8')).hexdigest()
        if not check.startswith('0000'):
            return False
    return True


def get_blockchain() -> List[Block]:
    return list(Block.objects.order_by('index'))


def get_blockchain_for_issuer(issuer: str) -> List[Block]:
    return list(Block.objects.filter(issuer=issuer).order_by('index'))


def add_certificate_to_blockchain(certificate_hash: str, issuer: str) -> Block:
    prev_block = get_previous_block()
    prev_proof = prev_block.nonce if prev_block else 1
    proof = proof_of_work(prev_proof)
    prev_hash = hash_block(prev_block) if prev_block else '0'
    block = create_block(proof=proof, previous_hash=prev_hash, certificate_hash=certificate_hash, issuer=issuer)
    return block


