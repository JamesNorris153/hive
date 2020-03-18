from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	""" Bee class

	Stores transactions using the Transaction class in blocks using the Blocks class.
	The blocks are linked together by storing the cryptographic hash of the previous
	block in each block.  New blocks must be mined using one of three methods, proof of
	work, proof of stake and proof of stake v2.  Bee's using the Bee class can mine new
	blocks.

	vars:
	address - (string) IP address of the node represented by the bee
	honeycomb - (integer) balance of the bee
	stakes - (list:(integer, integer)) list of stakes held on blocks of certain height
	key_pair - (Crypto.PublicKey.RSA.RsaKey) public-private key pair of the bee
	public_key - (bytes) byte representation of public key

	methods:
	add_stake(amount, height) - adds a stake of amount on a block at height
	calculate_balance(chain, index) - calculate bees balance at index of chain
	decrement_balance(amount) - decrements balance of bee by amount
	increment_balance(amount) - increments balance of bee by amount
	remove_stake(stake) - removes stake from bees current stakes
	"""

	def __init__(self, address, honeycomb):
		""" Constructs a Bee object.

		args:
		address - (string) IP address of the node represented by the bee
		honeycomb - (integer) balance of the bee
		"""
		self.address = address
		self.honeycomb = honeycomb
		self.stakes = []
		self.key_pair = RSA.generate(2048)
		self.public_key = self.key_pair.publickey().export_key()

	def add_stake(self, amount, height):
		""" Adds a stake on a block at a certain height and removes stake amount from
		bees balance.

		args:
		amount - (integer) amount to stake on block
		height - (height) block height at which to place stake
		"""
		self.stakes.append((amount, height))

	def calculate_balance(self, chain, index):
		""" Calculates the balance of the Bee object using a chain of blocks containing
		transactions.

		args:
		chain - (list:models.Block) chain of blocks to calculate balance from
		index - (integer) height at which to calculate balance to

		return:
		(integer) - the balance of the bee
		(list:(integer, integer)) - stakes placed by the bee at a certain block height
		"""
		self.honeycomb = 0
		self.stakes = []

		for block in chain[0:index]:
			if block.proof_type == "PoS2":
				if block.validator == self.address:
					self.add_stake(block.stake, block.index)
					self.decrement_balance(block.stake)

			for stake in self.stakes:
				if stake[1] + 2 <= block.index:
					self.remove_stake(stake)
					self.increment_balance(stake[0])

			for transaction in block.transactions:
				if transaction.sender == self.address:
					self.decrement_balance(int(transaction.amount))

				if transaction.recipient == self.address:
					self.increment_balance(int(transaction.amount))

		if self.honeycomb < 0:
			self.honeycomb = None
			return False

		return self.honeycomb, self.stakes

	def decrement_balance(self, amount):
		""" Decrements the balance of the bee by amount.

		args:
		amount - (integer) amount to decrement balance by
		"""
		self.honeycomb -= amount

	def increment_balance(self, amount):
		""" Increments the balance of the bee by amount.

		args:
		amount - (integer) amount to increment balance by
		"""
		self.honeycomb += amount

	def remove_stake(self, stake):
		""" Removes stake held on a block at a certain height and adds stake amount from
		bees balance.

		args:
		stake - (integer, integer) stake held on a block
		"""
		self.stakes.remove(stake)
