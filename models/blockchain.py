from .Block import Block
import time

class Blockchain:
	difficulty = 2
	timeslot = 10

	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = []
		self.create_genesis_block()

	def create_genesis_block(self):
		genesis_block = Block(0, [], time.time(), "OG")
		genesis_block.hash = genesis_block.compute_hash()
		self.chain.append(genesis_block)

	def last_block(self):
		return self.chain[-1]

	def proof_of_work(self, block):
		block.nonce = 0

		computed_hash = block.compute_hash()
		while not computed_hash.startswith('0' * Blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return computed_hash

	def proof_of_stake(self, block, stake):
		computed_hash = block.compute_hash()
		return proof_of_work(block)

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
		return (proof.startswith('0' * Blockchain.difficulty) and proof == block.compute_hash())

	def add_transaction(self, transaction):
		self.unconfirmed_transactions.append(transaction.__dict__)

	def mine(self):
		if not self.unconfirmed_transactions:
			return False

		last_block = self.last_block()

		new_block = Block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.compute_hash())

		proof = self.proof_of_stake(new_block)
		self.add_block(new_block, proof)
		self.unconfirmed_transactions = []
		return new_block.index
