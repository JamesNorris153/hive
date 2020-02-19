from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, address, honeycomb):
		self.address = address
		self.honeycomb = honeycomb
		self.key_pair = RSA.generate(2048)
		self.public_key = self.key_pair.publickey().export_key()

	def generate_key_pair(self):
		self.key_pair = RSA.generate(2048)

	def calculate_balance(self, chain, index):
		self.honeycomb = 0

		for block in chain[0:index]:
			for transaction in block.transactions:
				if transaction.sender == self.address:
					self.decrement_balance(int(transaction.amount))

				if transaction.recipient == self.address:
					self.increment_balance(int(transaction.amount))

		if self.honeycomb < 0:
			self.honeycomb = None
			return False


	def increment_balance(self, amount):
		self.honeycomb += amount

	def decrement_balance(self, amount):
		if self.honeycomb < amount:
			return False

		self.honeycomb -= amount
