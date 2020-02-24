from .Block import Block
from .Transaction import Transaction
from .Bee import Bee
import time
from hashlib import sha256

class Blockchain:
	difficulty = 2
	timeslot = 10
	threshold = "0000000999999999999999999999999999999999999999999999999999999999"

	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = []
		self.validators = []
		self.create_genesis_block()

	def create_genesis_block(self):
		transactions = []
		transactions.append(Transaction("god", "http://127.0.0.1:8000", 2000, 0))
		transactions.append(Transaction("god", "http://127.0.0.1:8001", 1000, 1))
		transactions.append(Transaction("god", "http://127.0.0.1:8002", 1000, 2))
		transactions.append(Transaction("god", "http://127.0.0.1:8003", 1000, 3))
		transactions.append(Transaction("god", "http://127.0.0.1:8004", 1000, 4))
		transactions.append(Transaction("god", "http://127.0.0.1:8005", 1000, 5))
		transactions.append(Transaction("god", "http://127.0.0.1:8006", 1000, 6))
		transactions.append(Transaction("god", "http://127.0.0.1:8007", 1000, 7))
		transactions.append(Transaction("god", "http://127.0.0.1:8008", 1000, 8))
		transactions.append(Transaction("god", "http://127.0.0.1:8009", 1000, 9))
		genesis_block = Block(0, transactions, time.time(), "OG", None, "god", 0)
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

	def proof_of_stake_v2(self, block, bee):
		block.stake = bee.calculate_balance(self.chain, block.index)
		block.validator = bee.address
		block.signature = block.sign_block(bee)

		time_passed = block.timestamp - self.last_block().timestamp
		computed_hash = block.compute_hash()

		while not int(computed_hash, 16) < (int(Blockchain.threshold, 16) * block.stake * time_passed):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return computed_hash

	def add_pow_block(self, block, proof):
		if not self.validate_block(block):
			return False

		if not self.validate_proof_of_work(block, proof):
			return False

		self.chain.append(block)

		return True

	def add_pos_block(self, block, proof):
		if not self.validate_block(block):
			return False

		if not self.validate_proof_of_stake(block, proof):
			return False

		block.signature = str(proof)
		self.chain.append(block)

		return True

	def add_pos_block_v2(self, block, proof):
		if not self.validate_block(block):
			print("invalid block")
			return False

		if not self.validate_proof_of_stake_v2(block, proof):
			print("invalid pos 2")
			return False

		self.chain.append(block)

		return True

	def validate_block(self, block):
		last_block = self.last_block()
		if block.index != (last_block.index + 1):
			print("invalid index")
			return False

		previous_hash = self.last_block().compute_hash()
		print(previous_hash)
		if previous_hash != block.previous_hash:
			print("invalid hash")
			return False

		return True

	def validate_proof_of_work(self, block, proof):
		return (proof.startswith('0' * Blockchain.difficulty) and proof == block.compute_hash())

	def validate_proof_of_stake(self, block, proof):
		next_validator = self.get_next_validator(block.index)
		return proof == next_validator.public_key

	def validate_proof_of_stake_v2(self, block, proof):
		if block.timestamp > time.time():
			return False

		time_passed = block.timestamp - self.last_block().timestamp
		validator = Bee(block.validator, 0)

		if validator.calculate_balance(self.chain, block.index) < block.stake:
			return False

		if proof != block.compute_hash():
			return False

		if int(proof, 16) >= (int(Blockchain.threshold, 16) * block.stake * time_passed):
			return False

		return True


	def add_transaction(self, transaction):
		for unconfirmed_transaction in self.unconfirmed_transactions:
			if transaction.timestamp == unconfirmed_transaction.timestamp:
				return False

		self.unconfirmed_transactions.append(transaction)
		return True


	def add_validator(self, bee):
		for validator in self.validators:
			if bee.address == validator.address:
				return False

		self.validators.append(bee)

	def mine_pow(self, bee):
		if not self.unconfirmed_transactions:
			return None, None

		last_block = self.last_block()
		new_block = Block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), proof_type="PoW", validator=bee.address, previous_hash=last_block.compute_hash())

		proof = self.proof_of_work(new_block)

		self.add_pow_block(new_block, proof)
		self.unconfirmed_transactions = []

		return proof, new_block

	def mine_pos(self, bee):
		if not self.unconfirmed_transactions:
			return None, None

		last_block = self.last_block()
		new_block = Block(index=last_block.index + 1,  transactions=self.unconfirmed_transactions, timestamp=time.time(), proof_type="PoS", validator=bee.address, previous_hash=last_block.compute_hash())

		next_validator = self.get_next_validator(new_block.index)

		if next_validator != bee:
			return None, None

		proof = self.proof_of_stake(new_block, bee)
		self.add_pos_block(new_block, proof)
		self.unconfirmed_transactions = []

		return proof, new_block

	def mine_pos_v2(self, bee):
		if not self.unconfirmed_transactions:
			return None, None

		last_block = self.last_block()
		new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), proof_type="PoS2", validator=bee.address, previous_hash=last_block.compute_hash(), stake=bee.calculate_balance(self.chain, last_block.index))

		print(last_block.compute_hash())

		proof = self.proof_of_stake_v2(new_block, bee)
		self.add_pos_block_v2(new_block, proof)
		self.unconfirmed_transactions = []

		return proof, new_block


	def get_next_validator(self, index):
		self.calculate_validator_stakes(index)
		next_validator = self.validators[0]

		for validator in self.validators:
			if validator.honeycomb > next_validator.honeycomb:
				next_validator = validator

		return next_validator

	def calculate_validator_stakes(self, index):
		for validator in self.validators:
			validator.calculate_balance(self.chain, index)

	def check_validity(self):
		for block in self.chain:
			sender = Bee(block.validator, None)
			recipient = Bee(block.validator, None)

			self.add_validator(sender)
			self.add_validator(recipient)

			if block.proof_type == "PoW":
				proof = block.compute_hash()
				if not self.validate_proof_of_work(block, proof):
					return False

			if block.proof_type == "PoS":
				proof = block.signature
				if not self.validate_proof_of_stake(block, proof):
					return False

			if block.proof_type == "PoS2":
				proof = block.compute_hash()
				if not self.validate_proof_of_stake_v2(block, proof):
					return False

		return True

	def parse_json(self, chain):
		self.chain = []

		for block_data in chain:
			transactions = []
			for transaction in block_data["transactions"]:
				transactions.append(Transaction(transaction["sender"], transaction["recipient"], transaction["amount"], transaction["timestamp"]))

			block = Block(block_data["index"], transactions, block_data["timestamp"], block_data["previous_hash"], block_data["proof_type"], block_data["validator"], block_data["signature"], block_data["nonce"])

			self.chain.append(block)
