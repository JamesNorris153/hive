import json
from hashlib import sha256

class Block:
	def __init__(self, index, transactions, timestamp, previous_hash, proof_type, validator, signature=None, nonce=0):
		self.index = index
		self.transactions = transactions
		self.timestamp = timestamp
		self.previous_hash = previous_hash
		self.proof_type = proof_type
		self.validator = validator
		self.signature = signature
		self.nonce = nonce

	def compute_hash(self):
		block_string = json.dumps(self.to_dict(), sort_keys=True)
		return sha256(block_string.encode()).hexdigest()

	def sign_block(self, validator):
		self.signature = validator.key_pair.publickey().export_key()

	def to_dict(self):
		block_dict = dict()
		block_dict["index"] = self.index
		block_dict["transactions"] = []
		for transaction in self.transactions:
			block_dict["transactions"].append(transaction.__dict__)
		block_dict["timestamp"] = self.timestamp
		block_dict["previous_hash"] = self.previous_hash
		block_dict["proof_type"] = self.proof_type
		block_dict["validator"] = self.validator
		block_dict["signature"] = self.signature
		block_dict["nonce"] = self.nonce
		return block_dict
