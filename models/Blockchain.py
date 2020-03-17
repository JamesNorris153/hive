from .Block import Block
from .Transaction import Transaction
from .Bee import Bee
import time
from hashlib import sha256

class Blockchain:
	""" Blockchain class

	Stores transactions using the Transaction class in blocks using the Blocks class.
	The blocks are linked together by storing the cryptographic hash of the previous
	block in each block.  New blocks must be mined using one of three methods, proof of
	work, proof of stake and proof of stake v2.  Bee's using the Bee class can mine new
	blocks.

	vars:
	chain - ordered list of all blocks
	stake - the total stake placed on the blockchain
	unconfirmed_transactions - list of transactions to be mined into a block
	validators - list of bee's that can mine on the blockchain

	methods:
	add_pow_block(block, proof) - adds a proof of work block to the chain
	add_pos_block(block, proof) - adds a proof of stake block to the chain
	add_pos_block_v2(block, proof) - adds a proof of stake v2 block to the chain
	add_transactions(transaction) - adds transaction to list of unconfirmed transactions
	add_validator(bee) - adds validator to list of validators
	calculate_validator_stakes(index) - calculates the stakes of each validator
	check_validity() - confirms validity of the blockchain
	create_genesis_block() - generates the first block in the blockchain
	get_next_validator(index) - finds next validator for proof of stake
	last_block() - returns the last block in the chain
	mine_pos(bee, stake) - mines unconfirmed transactions into a block using proof of
	stake
	mine_pos_v2(bee, stake) - mines unconfirmed transactions into a block using proof of
	stake v2
	mine_pow(bee) - mines unconfirmed transactions into a block using proof of work
	parse_json(chain) - sets blockchain data based of a json
	proof_of_stake(block, bee) - creates a valid block using proof of stake
	proof_of_stake_v2(block, bee) - creates a valid block using proof of stake v2
	proof_of_work(block) - creates a valid block using proof of work
	validate_block(block) - validates a block based on its index and hash
	validate_proof_of_stake(block, previous_block, proof) - validates block's proof of
	stake
	validate_proof_of_stake_v2(block, previous_block, proof) - validates a block's proof
	of stake v2
	validate_proof_of_work(block, proof) - validates block's proof of work
	verify_transaction(transaction) - verifies transaction
	"""
	difficulty = 2
	timeslot = 10
	threshold = "0000999999999999999999999999999999999999999999999999999999999999"

	def __init__(self):
		""" Constucts a Blockchain object """
		self.chain = []
		self.stake = 0
		self.unconfirmed_transactions = []
		self.validators = []
		self.create_genesis_block()

	def add_pow_block(self, block, proof):
		""" Adds Block object mined using proof of work to the chain.

		args:
		block - (models.Block) Block object to be added to the chain
		proof - (string) cryptographic hash of block to be added

		return:
		(boolean) true or false depending on whether block was added to the chain
		"""
		if not self.validate_block(block):
			return False
		if not self.validate_proof_of_work(block, proof):
			return False

		self.chain.append(block)
		self.stake += block.stake
		self.unconfirmed_transactions = []
		return True

	def add_pos_block(self, block, proof):
		""" Adds Block object mined using proof of stake to the chain.

		args:
		block - (models.Block) Block object to be added to the chain
		proof - (string) public key of miner of the block to be added

		return:
		(boolean) true or false depending on whether block was added to the chain
		"""
		if not self.validate_block(block):
			return False
		if not self.validate_proof_of_stake(block, self.last_block(), proof):
			return False

		self.chain.append(block)
		self.stake += block.stake
		self.unconfirmed_transactions = []
		return True

	def add_pos_block_v2(self, block, proof):
		""" Adds Block object mined using proof of stake v2 to the chain.

		args:
		block - (models.Block) Block object to be added to the chain
		proof - (string) cryptographic hash of the block to be added

		return:
		(boolean) true or false depending on whether block was added to the chain
		"""
		if not self.validate_block(block):
			return False
		if not self.validate_proof_of_stake_v2(block, self.last_block(), proof):
			return False

		self.chain.append(block)
		self.stake += block.stake
		self.unconfirmed_transactions = []
		return True

	def add_transaction(self, transaction):
		""" Adds Transaction object to list of unconfirmed transactions.

		args:
		block - (models.Transactions) Transaction object to be added to the unconfirmed
		transaction list

		return:
		(boolean) true or false depending on whether transactions was added to
		unconfirmed transaction list
		"""
		for unconfirmed_transaction in self.unconfirmed_transactions:
			if transaction.timestamp == unconfirmed_transaction.timestamp:
				return False

		self.unconfirmed_transactions.append(transaction)
		return True


	def add_validator(self, bee):
		""" Adds a Bee object to list of validators.

		args:
		bee - (models.Transactions) Bee object to be added to the list of validators

		return:
		(boolean) true or false depending on whether bee was added to list of validators
		"""
		for validator in self.validators:
			if bee.address == validator.address:
				return False

		self.validators.append(bee)
		return True

	def calculate_validator_stakes(self, index):
		""" Calculates stakes currently placed by validators.

		args:
		index - (integer) chain height at which to calculate stakes
		"""
		for validator in self.validators:
			validator.calculate_balance(self.chain, index)

	def check_validity(self):
		""" Checks the validity of the blockchain.

		return:
		(boolean) - validity of the blockchain
		"""
		previous_block = None
		for block in self.chain:
			validator = Bee(block.validator, None)
			self.add_validator(validator)

			if block.proof_type == "PoW":
				proof = block.compute_hash()
				if not self.validate_proof_of_work(block, proof):
					return False
			if block.proof_type == "PoS":
				proof = block.signature
				if not self.validate_proof_of_stake(block, previous_block, proof):
					return False
			if block.proof_type == "PoS2":
				proof = block.compute_hash()
				if not self.validate_proof_of_stake_v2(block, previous_block, proof):
					return False
			previous_block = block
		return True

	def create_genesis_block(self):
		""" Creates and adds the first block to the blockchain, distributes currencies to
		selected nodes.
		"""
		transactions = []
		transactions.append(Transaction("james", "http://127.0.0.1:8000", 1000, 0))
		transactions.append(Transaction("james", "http://127.0.0.1:8001", 1000, 1))
		transactions.append(Transaction("james", "http://127.0.0.1:8002", 1000, 2))
		transactions.append(Transaction("james", "http://127.0.0.1:8003", 1000, 3))
		transactions.append(Transaction("james", "http://127.0.0.1:8004", 1000, 4))
		genesis_block = Block(0, transactions, 1582578648.950698, "OG", None, "james", 0)
		self.chain.append(genesis_block)

	def get_next_validator(self, index):
		""" Finds validator with the highest balance

		args:
		index - (integer) chain height at which to find the validator

		return:
		(models.Bee) - validator with the highest balance
		"""
		self.calculate_validator_stakes(index)
		next_validator = self.validators[0]
		for validator in self.validators:
			if validator.honeycomb > next_validator.honeycomb:
				next_validator = validator

		return next_validator

	def last_block(self):
		""" Returns the last block in the blockchain

		return:
		(models.Block) - last block in chain
		"""
		return self.chain[-1]

	def mine_pos(self, bee, stake):
		""" Mines unconfirmed transactions into the next block using proof of stake.

		args:
		bee - (models.Bee) Bee object mining the new block
		stake - (integer) stake being used to mine the block

		return:
		(string) - public key of bee mining the block
		(models.Block) - block mined using proof of stake
		"""
		if not self.unconfirmed_transactions:
			return None, None

		self.calculate_validator_stakes(self.last_block().index + 1)
		for transaction in self.unconfirmed_transactions:
			if not self.verify_transaction(transaction):
				self.unconfirmed_transactions.remove(transaction)

		last_block = self.last_block()
		new_block = Block(
			index=last_block.index + 1,
			transactions=self.unconfirmed_transactions,
			timestamp=time.time(),
			proof_type="PoS",
			validator=bee.address,
			previous_hash=last_block.compute_hash(),
			stake=int(stake)
		)

		#next_validator = self.get_next_validator(new_block.index)

		#if next_validator != bee:
		#	return None, new_block

		proof = self.proof_of_stake(new_block, bee)
		self.add_pos_block(new_block, proof)
		return proof, new_block

	def mine_pos_v2(self, bee, stake):
		""" Mines unconfirmed transactions into the next block using proof of stake v2.

		args:
		bee - (models.Bee) Bee object mining the new block
		stake - (integer) stake being used to mine the block

		return:
		(string) - cryptographic hash of mined block
		(models.Block) - block mined using proof of stake v2
		"""
		if not self.unconfirmed_transactions:
			return None, None

		self.calculate_validator_stakes(self.last_block().index + 1)
		for transaction in self.unconfirmed_transactions:
			if not self.verify_transaction(transaction):
				self.unconfirmed_transactions.remove(transaction)

		last_block = self.last_block()
		new_block = Block(
			index=last_block.index + 1,
			transactions=self.unconfirmed_transactions,
			timestamp=time.time(),
			proof_type="PoS2",
			validator=bee.address,
			previous_hash=last_block.compute_hash(),
			stake=int(stake)
		)

		proof = self.proof_of_stake_v2(new_block, bee)
		self.add_pos_block_v2(new_block, proof)
		return proof, new_block

	def mine_pow(self, bee):
		""" Mines unconfirmed transactions into the next block using proof of work.

		args:
		bee - (models.Bee) Bee object mining the new block

		return:
		(string) - cryptographic hash of mined block
		(models.Block) - block mined using proof of work
		"""
		if not self.unconfirmed_transactions:
			return None, None

		self.calculate_validator_stakes(self.last_block().index + 1)
		for transaction in self.unconfirmed_transactions:
			if not self.verify_transaction(transaction):
				self.unconfirmed_transactions.remove(transaction)

		last_block = self.last_block()
		new_block = Block(
			index=last_block.index + 1,
			transactions=self.unconfirmed_transactions,
			timestamp=time.time(),
			proof_type="PoW",
			validator=bee.address,
			previous_hash=last_block.compute_hash(),
			stake=0
		)

		proof = self.proof_of_work(new_block)
		self.add_pow_block(new_block, proof)
		return proof, new_block

	def parse_json(self, chain):
		""" Sets the data of the chain given a json representation of the chain.

		args:
		chain - (string) json representation of chain
		"""
		self.chain = []

		for block_data in chain:
			transactions = []
			for transaction in block_data["transactions"]:
				transactions.append(Transaction(
					transaction["sender"],
					transaction["recipient"],
					transaction["amount"],
					transaction["timestamp"]
				))

			block = Block(
				index=block_data["index"],
				transactions=transactions,
				timestamp=block_data["timestamp"],
				previous_hash=block_data["previous_hash"],
				proof_type=block_data["proof_type"],
				validator=block_data["validator"],
				stake=block_data["stake"],
				signature=block_data["signature"],
				nonce=block_data["nonce"]
			)

			self.chain.append(block)
			self.stake += block.stake

	def proof_of_stake(self, block, bee):
		""" Validates a new block using proof of stake.

		args:
		block - (models.Block) Block object to be validated
		bee - (models.Bee) Bee object validating the block

		return:
		(string or boolean) - public key of validating bee or false if bee does not have
		enough stake
		"""
		block.validator = bee.address
		block.sign_block(bee)
		validator = Bee(block.validator, 0)
		honeycomb, stakes = validator.calculate_balance(self.chain, block.index)
		if honeycomb < block.stake:
			return False

		return bee.key_pair.publickey().export_key()

	def proof_of_stake_v2(self, block, bee):
		""" Validates a new block using proof of stake v2.

		args:
		block - (models.Block) Block object to be validated
		bee - (models.Bee) Bee object validating the block

		return:
		(string or boolean) - cryptographic hash of mined block or false if bee does not
		have enough stake
		"""
		block.validator = bee.address
		block.sign_block(bee)
		validator = Bee(block.validator, 0)
		honeycomb, stakes = validator.calculate_balance(self.chain, block.index)
		if honeycomb < block.stake:
			return False

		time_passed = block.timestamp - self.last_block().timestamp
		computed_hash = block.compute_hash()
		block.nonce = 0
		while not int(computed_hash, 16) < (int(Blockchain.threshold, 16) * block.stake * time_passed):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return computed_hash

	def proof_of_work(self, block):
		""" Validates a new block using proof of work.

		args:
		block - (models.Block) Block object to be validated

		return:
		(string) - cryptographic hash of mined block
		"""
		block.nonce = 0
		computed_hash = block.compute_hash()
		while not computed_hash.startswith('0' * Blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return computed_hash

	def validate_block(self, block):
		""" Checks whether a blocks index and hash are valid.

		args:
		block - (models.Block) Block object to be validated

		return:
		(boolean) - validity of block
		"""
		last_block = self.last_block()
		if block.index != (last_block.index + 1):
			return False

		previous_hash = self.last_block().compute_hash()
		if previous_hash != block.previous_hash:
			return False

		return True

	def validate_proof_of_stake(self, block, previous_block, proof):
		""" Verifies whether a blocks proof of stake is valid.

		args:
		block - (models.Block) Block object to be validated
		previous_block - (models.Block) Block object previous to block
		proof - (string) public key of block's validating bee

		return:
		(boolean) - validity of proof of stake
		"""
		if block.timestamp > time.time():
			return False

		validator = Bee(block.validator, 0)
		honeycomb, stakes = validator.calculate_balance(self.chain, block.index)
		if honeycomb < block.stake:
			return False

		return True

	def validate_proof_of_stake_v2(self, block, previous_block, proof):
		""" Verifies whether a blocks proof of stake v2 is valid.

		args:
		block - (models.Block) Block object to be validated
		previous_block - (models.Block) Block object previous to block
		proof - (string) cryptographic hash of block

		return:
		(boolean) - validity of proof of stake v2
		"""
		if block.timestamp > time.time():
			return False

		time_passed = block.timestamp - previous_block.timestamp
		validator = Bee(block.validator, 0)
		honeycomb, stakes = validator.calculate_balance(self.chain, block.index)
		if honeycomb < block.stake:
			return False
		if proof != block.compute_hash():
			return False
		if int(proof, 16) >= (int(Blockchain.threshold, 16) * block.stake * time_passed):
			return False

		return True

	def validate_proof_of_work(self, block, proof):
		""" Verifies whether a blocks proof of work is valid.

		args:
		block - (models.Block) Block object to be validated
		proof - (string) cryptographic hash of block

		return:
		(boolean) - validity of proof of work
		"""
		return (proof.startswith('0' * Blockchain.difficulty)
				and proof == block.compute_hash())

	def verify_transaction(self, transaction):
		""" Verifies whether a transaction is valid.

		args:
		transaction - (models.Transaction) Transaction object to be verified

		return:
		(boolean) - validity of transaction
		"""
		sender = Bee(transaction.sender, None)
		if not self.add_validator(sender):
			sender.calculate_balance(self.chain, self.last_block().index + 1)

		if sender.honeycomb < int(transaction.amount):
			return False

		return True
