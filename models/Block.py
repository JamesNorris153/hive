import json
from hashlib import sha256

class Block:
	""" Block class

	Stores transactions using the Transaction class into a list.  Stores the
	cryptographic hash of a previous block in order to form a chain of blocks.  The block
	also stores header data that is used in ensuring the block is valid.

	vars:
	index - (integer) height of the block in the chain
	previous_hash - (string) cryptographic hash of the previous block in the chain
	proof_type - (string) type of proof used to validate the block
	stake - (integer) amount of honeycomb staked on the block
	timestamp - (float) time at which the block is created
	transactions - (list:models.Transaction) list of transactions stored in the block
	validator - (string) address of the bee validating the block
	nonce - (integer) arbitrary data used to change the hash of the block
	signature - (bytes) public key of the bee validating the block

	methods:
	compute_hash() - computes the cryptographic hash of the block
	sign_block(validator) - signs block with the validators signature
	to_dict() - returns a python dictionary representation of the block
	"""

	def __init__(
			self, index, previous_hash, proof_type, stake, timestamp, transactions,
			validator, nonce=0, signature=None
		):
		""" Constructs a Block object.

		args:
		index - (integer) height of the block in the chain
		previous_hash - (string) cryptographic hash of the previous block in the chain
		proof_type - (string) type of proof used to validate the block
		stake - (integer) amount of honeycomb staked on the block
		timestamp - (float) time at which the block is created
		transactions - (list:models.Transaction) list of transactions stored in the block
		validator - (string) address of the bee validating the block
		nonce - (integer) arbitrary data used to change the hash of the block
		signature - (bytes) public key of the bee validating the block
		"""
		self.index = index
		self.previous_hash = previous_hash
		self.proof_type = proof_type
		self.stake = stake
		self.timestamp = timestamp
		self.transactions = transactions
		self.validator = validator
		self.nonce = nonce
		self.signature = signature

	def compute_hash(self):
		""" Computes and returns the cryptographic hash representation of the block.

		return:
		(string) - cryptographic hash representation of the block
		"""
		block_string = json.dumps(self.to_dict(), sort_keys=True)
		return sha256(block_string.encode()).hexdigest()

	def sign_block(self, validator):
		""" Sets the signature of the block to the public key of the validating bee.

		args:
		validator - (bytes) public key of the validating bee
		"""
		self.signature = str(validator.key_pair.publickey().export_key())

	def to_dict(self):
		""" Returns a python dictionary representing the data contained in the block.

		return:
		(dict) public key of the validating bee
		"""
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
		block_dict["stake"] = self.stake
		return block_dict
