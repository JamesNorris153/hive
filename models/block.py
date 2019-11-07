import json
from hashlib import sha256

class block:
	def __init__(self, index, transactions, timestamp):
		self.index = []
		self.transactions = transactions
		self.timestamp = timestamp

	def compute_hash(self):
		block_string = json.dumps(self.__dict__, sort_keys = True)
		return sha256(block_string.encode()).hexdigest()
