import json
from hashlib import sha256

class Block:
	def __init__(self, index, transactions, timestamp, previous_hash, proof_type, nonce=0):
		self.index = index
		self.transactions = transactions
		self.timestamp = timestamp
		self.previous_hash = previous_hash
		self.proof_type = proof_type
		self.signature = None
		self.nonce = nonce

	def compute_hash(self):
		block_string = json.dumps(self.__dict__, sort_keys = True)
		return sha256(block_string.encode()).hexdigest()

	def sign_block(self, validator):
		self.signature = validator.key_pair.PublicKey
