from .block import block
import time

class blockchain:
	difficulty = 5

	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = []
		self.create_genesis_block()

	def create_genesis_block(self):
		genesis_block = block(0, [], time.time(), "0")
		genesis_block.hash = genesis_block.compute_hash()
		self.chain.append(genesis_block)

	def last_block(self):
		return self.chain[-1]

	def proof_of_work(self, block):
		block.nonce = 0

		computed_hash = block.compute_hash()
		while not computed_hash.startswith('0' * blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return computed_hash

	def add_block(self, block, proof):
		previous_hash = self.last_block().compute_hash()

		if previous_hash != block.previous_hash:
			return False

		if not self.validate_proof(block, proof):
			return False

		block.hash = proof
		self.chain.append(block)
		return True

	def validate_proof(self, block, proof):
		return (proof.startswith('0' * blockchain.difficulty) and proof == block.compute_hash())

	def add_new_transaction(self, transaction):
		self.unconfirmed_transactions.append(transaction)

	def mine(self):
		if not self.unconfirmed_transactions:
			return False

		last_block = self.last_block()

		new_block = block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.compute_hash())

		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		self.unconfirmed_transactions = []
		return new_block.index
