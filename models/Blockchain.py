import time
from .Bee import Bee
from .Block import Block
from hashlib import sha256
from .Transaction import Transaction

class Blockchain:
	""" Blockchain class

	Stores transactions using the Transaction class in blocks using the Blocks class.
	The blocks are linked together by storing the cryptographic hash of the previous
	block in each block.  New blocks must be mined using one of three methods, proof of
	work, proof of stake and proof of stake v2.  Bee's using the Bee class can mine new
	blocks.

	vars:
	chain - (list:models.Block) ordered list of all blocks
	stake - (integer) the total stake placed on the blockchain
	unconfirmed_transactions - (list:models.Transaction) list of transactions to be mined
	into a block
	bees - (list:models.Bee) list of bee's that can mine on the blockchain

	methods:
	add_bee(bee) - adds bee to list of bees
	add_pow_block(block, proof) - adds a proof of work block to the chain
	add_pos_block(block, proof) - adds a proof of stake block to the chain
	add_pos_block_v2(block, proof) - adds a proof of stake v2 block to the chain
	add_transactions(transaction) - adds transaction to list of unconfirmed transactions
	calculate_bee_balances(index) - calculates the balance of every bee
	create_genesis_block() - generates the first block in the blockchain
	get_next_bee(index) - finds next bee for proof of stake
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
	validate_proof_of_stake(block, previous_block, proof) - validates block's proof of3
	stake
	validate_proof_of_stake_v2(block, previous_block, proof) - validates a block's proof
	of stake v2
	validate_proof_of_work(block, proof) - validates block's proof of work
	verify_chain() - confirms validity of the blockchain
	verify_transaction(transaction) - verifies transaction
	"""
	difficulty = 4
	timeslot = 10
	threshold = "0000999999999999999999999999999999999999999999999999999999999999"

	def __init__(self):
		""" Constucts a Blockchain object """
		self.chain = []
		self.stake = 0
		self.unconfirmed_transactions = []
		self.create_genesis_block()

	#def add_bee(self, bee):
		#""" Adds bee to list of bees.

		#args:
		#bee - (models.Bee) bee to be added to the list of bee

		#return:
		#(boolean) true or false depending on whether bee was added to list of bees
		#"""
		#for known_bee in self.bees:
		#	if bee.address == known_bee.address:
		#		return False

		#bee.calculate_balance(self.chain, self.last_block().index + 1)
		#self.bees.append(bee)
		#return True

	def add_block(self, block):
		""" Adds block object to the end of the chain.

		args:
		block - (models.Block) block to be added to the chain
		"""
		self.chain.append(block)
		self.stake += int(block.stake)
		self.unconfirmed_transactions = []

	def add_transaction(self, transaction):
		""" Adds transaction to list of unconfirmed transactions.

		args:
		transaction - (models.Transactions) transaction to be added to the unconfirmed
		transaction list
		"""
		for unconfirmed_transaction in self.unconfirmed_transactions:
			if transaction.timestamp == unconfirmed_transaction.timestamp:
				return False
		self.unconfirmed_transactions.append(transaction)
		return True

	#def calculate_bee_balances(self, index):
		#""" Calculates stakes currently placed by bees.

		#args:
		#index - (integer) chain height at which to calculate stakes
		#"""
		#for bee in self.bees:
		#	bee.calculate_balance(self.chain, index)

	def create_genesis_block(self):
		""" Creates and adds the first block to the blockchain, distributes currencies to
		selected nodes.
		"""
		transactions = []
		transactions.append(Transaction(1000, "http://127.0.0.1:8000", "james", 0))
		transactions.append(Transaction(1000, "http://127.0.0.1:8001", "james", 1))
		transactions.append(Transaction(1000, "http://127.0.0.1:8002", "james", 2))
		transactions.append(Transaction(1000, "http://127.0.0.1:8003", "james", 3))
		transactions.append(Transaction(1000, "http://127.0.0.1:8004", "james", 4))

		genesis_block = Block(
			index=0,
			previous_hash=0,
			proof_type="Na",
			stake=0,
			timestamp=1582578648.950698,
			transactions=transactions,
			validator="God",
			nonce=0,
			signature="God"
		)

		genesis_block.previous_hash = genesis_block.compute_hash()
		self.chain.append(genesis_block)

	#def get_next_bee(self, index):
		#""" Finds bee with the highest balance

		#args:
		#index - (integer) chain height at which to find the bee

		#return:
		#(models.Bee) - bee with the highest balance
		#"""
		#self.calculate_bee_balances(index)
		#next_bee = self.bees[0]
		#for bee in self.bees:
		#	if bee.honeycomb > next_bee.honeycomb:
		#		next_bee = bee

		#return next_bee

	def last_block(self):
		""" Returns the last block in the blockchain.

		return:
		(models.Block) - last block in chain
		"""
		return self.chain[-1]

	def mine_block(self, bee, proof_type, stake):
		""" Mines the list of unconfirmed transaction into a block using proof of stake
		version one or two or proof of work.

		args:
		proof_type - (string) type of proof used to mine the transactions
		bee - (string) address of bee mining the block
		stake - (integer) amount of stake used in the proof of stake protocols

		return:
		(models.Block) - the mined block
		"""
		if not self.unconfirmed_transactions:
			return None

		last_block = self.last_block()
		new_block = Block(
			index=last_block.index + 1,
			previous_hash=last_block.compute_hash(),
			proof_type=proof_type,
			stake=stake,
			timestamp=time.time(),
			transactions=self.unconfirmed_transactions,
			validator=bee
		)

		if proof_type == "PoS":
			return self.proof_of_stake(new_block)
		elif proof_type == "PoS2":
			return self.proof_of_stake_v2(new_block)
		elif proof_type == "PoW":
			return self.proof_of_work(new_block)

	def parse_json(self, chain):
		""" Sets the data of the chain given a json representation of the chain.

		args:
		chain - (string) json representation of chain
		"""
		self.chain = []

		for block_data in chain:
			transactions = []
			for transaction in block_data["transactions"]:
				transactions.append(
					Transaction(
						amount=transaction["amount"],
						recipient=transaction["recipient"],
						sender=transaction["sender"],
						timestamp=transaction["timestamp"]
					)
				)

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

	def proof_of_stake(self, block):
		""" Validates a new block using proof of stake.

		args:
		block - (models.Block) block to be validated

		return:
		(models.Block) - validated block
		"""
		bee = Bee(address=block.validator, honeycomb=0)
		honeycomb, stakes = bee.calculate_balance(self.chain, block.index)
		if honeycomb < int(block.stake):
			return None

		return block

	def proof_of_stake_v2(self, block):
		""" Validates a new block using proof of stake v2.

		args:
		block - (models.Block) block to be validated

		return:
		(models.Block) - validated block
		"""
		bee = Bee(address=block.validator, honeycomb=0)
		honeycomb, stakes = bee.calculate_balance(self.chain, block.index)
		if honeycomb < block.stake:
			return None

		computed_hash = block.compute_hash()
		while not int(computed_hash, 16) < (int(Blockchain.threshold, 16)
											* block.stake):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return block

	def proof_of_work(self, block):
		""" Validates a new block using proof of work.

		args:
		block - (models.Block) block to be validated

		return:
		(models.Block) - validated block
		"""
		computed_hash = block.compute_hash()
		while not computed_hash.startswith('0' * Blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()

		return block

	#def update_balances(self, transaction):
	#	for sender in self.bees:
	#		if sender.address == transaction.sender:
	#			sender.decrement_balance(int(transaction.amount))

	#	for recipient in self.bees:
	#		if recipient.address == transaction.recipient:
	#			recipient.increment_balance(int(transaction.amount))

	def verify_block(self, block, previous_block):
		""" Verifies that a block is valid.

		args:
		block - (models.Block) Block object to be validated

		return:
		(boolean) - validity of block
		"""
		previous_hash = previous_block.compute_hash()
		if block.index != (previous_block.index + 1):
			return False
		elif block.timestamp < previous_block.timestamp:
			return False
		elif block.timestamp > time.time():
			return False
		elif block.previous_hash != previous_hash:
			return False

		for transaction in block.transactions:
			if not self.verify_transaction(transaction):
				return False

		if block.proof_type == "PoS":
			return self.verify_pos(block)
		elif block.proof_type == "PoS2":
			return self.verify_pos_v2(block)
		elif block.proof_type == "PoW":
			return self.verify_pow(block)
		else:
			return False

	def verify_chain(self):
		""" Verifies that the blockchain is valid.

		return:
		(boolean) - validity of the blockchain
		"""
		previous_block = self.chain[0]
		chain = iter(self.chain)
		next(chain)
		for block in chain:
			if not self.verify_block(block, previous_block):
				return False
			previous_block = block
		return True

	def verify_pos(self, block):
		""" Verifies whether a blocks proof of stake is valid.

		args:
		block - (models.Block) Block object to be verified

		return:
		(boolean) - validity of proof of stake
		"""
		bee = Bee(address=block.validator, honeycomb=0)
		honeycomb, stakes = bee.calculate_balance(self.chain, block.index)
		return honeycomb >= block.stake

	def verify_pos_v2(self, block):
		""" Verifies whether a blocks proof of stake v2 is valid.

		args:
		block - (models.Block) Block object to be validated

		return:
		(boolean) - validity of proof of stake v2
		"""
		bee = Bee(address=block.validator, honeycomb=0)
		honeycomb, stakes = bee.calculate_balance(self.chain, block.index)
		computed_hash = block.compute_hash()
		return (honeycomb > block.stake) and (int(computed_hash, 16)
												<=
												(int(Blockchain.threshold, 16)
												* block.stake))

	def verify_pow(self, block):
		""" Verifies whether a blocks proof of work is valid.

		args:
		block - (models.Block) Block object to be validated

		return:
		(boolean) - validity of proof of work
		"""
		return (block.compute_hash().startswith('0' * Blockchain.difficulty))

	def verify_transaction(self, transaction):
		""" Verifies whether a transaction is valid.

		args:
		transaction - (models.Transaction) Transaction object to be verified

		return:
		(boolean) - validity of transaction
		"""
		sender = Bee(transaction.sender, 0)
		sender.calculate_balance(self.chain, self.last_block().index + 1)

		return sender.honeycomb >= int(transaction.amount)
