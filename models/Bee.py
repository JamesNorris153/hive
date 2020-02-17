from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, address, honeycomb):
		self.address = address
		self.honeycomb = honeycomb
		self.key_pair = None

	def generate_key_pair(self):
		self.key_pair = RSA.generate(2048)

	def calculate_balance(self, blockchain):
		self.honeycomb = 0

		for block in blockchain.chain:
			for transaction in block.transactions:
				if transaction.sender == self.address:
					self.decrement_balance(transaction.amount)

				if transaction.recipient == self.address:
					self.increment_balance(transaction.amount)

		if self.honeycomb < 0:
			self.honeycomb = None
			return False


	def increment_balance(self, amount):
		self.honeycomb += amount

	def decrement_balance(self, amount):
		if self.honeycomb < amount:
			return False

		self.honeycomb -= amount
