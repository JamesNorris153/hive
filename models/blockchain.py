from .Block import Block
from .Transaction import Transaction
import time

class Blockchain:
	difficulty = 2
	timeslot = 10

	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = []
		self.validators = []
		self.create_genesis_block()

	def create_genesis_block(self):
		transactions = []
		transactions.append(Transaction("god", "http://127.0.0.1:8000", 1000, 1))
		transactions.append(Transaction("god", "http://127.0.0.1:8001", 500, 2))
		genesis_block = Block(0, transactions, 0, "OG", 1)
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

	def proof_of_stake(self, block, bee):
		block.sign_block(bee)
		return bee.key_pair.publickey().export_key()

	def add_pow_block(self, block, proof):
		previous_hash = self.last_block().compute_hash()

		if previous_hash != block.previous_hash:
			print(previous_hash)
			print(block.previous_hash)
			print("wow")
			return False

		if not self.validate_proof_of_work(block, proof):
			print("fuck")
			return False

		self.chain.append(block)

		return True

	def add_pos_block(self, block, proof):
		previous_hash = self.last_block().compute_hash()

		if previous_hash != block.previous_hash:
			print(previous_hash)
			print(block.previous_hash)
			return False

		if not self.validate_proof_of_stake(proof):
			return False

		block.signature = str(proof)
		self.chain.append(block)

		return True

	def validate_proof_of_work(self, block, proof):
		return (proof.startswith('0' * Blockchain.difficulty) and proof == block.compute_hash())

	def validate_proof_of_stake(self, proof):
		next_validator = self.get_next_validator()
		return str(proof) == str(next_validator.public_key)

	def add_transaction(self, transaction):
		self.unconfirmed_transactions.append(transaction)

	def add_transaction(self, sender, recipient, amount, time):
		transaction = Transaction(sender, recipient, amount, time)
		self.unconfirmed_transactions.append(transaction)

	def add_validator(self, bee):
		self.validators.append(bee)

	def mine_pow(self):
		if not self.unconfirmed_transactions:
			return False

		last_block = self.last_block()
		new_block = Block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), proof_type="PoW", previous_hash=last_block.compute_hash())

		proof = self.proof_of_work(new_block)

		self.add_pow_block(new_block, proof)
		self.unconfirmed_transactions = []

		return proof, new_block

	def mine_pos(self, bee):
		if not self.unconfirmed_transactions:
			return False

		last_block = self.last_block()
		new_block = Block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), proof_type="PoS", previous_hash=last_block.compute_hash())

		next_validator = self.get_next_validator()

		if next_validator != bee:
			return False, None

		proof = self.proof_of_stake(new_block, bee)
		self.add_pos_block(new_block, proof)
		self.unconfirmed_transactions = []

		return proof, new_block

	def get_next_validator(self):
		self.refresh_validator_stakes()
		next_validator = self.validators[0]

		for validator in self.validators:
			if validator.honeycomb > next_validator.honeycomb:
				next_validator = validator

		return next_validator

	def refresh_validator_stakes(self):
		for validator in self.validators:
			validator.calculate_balance(self.chain)
