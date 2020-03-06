from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, address, honeycomb):
		self.address = address
		self.honeycomb = honeycomb
		self.stakes = []
		self.key_pair = RSA.generate(2048)
		self.public_key = self.key_pair.publickey().export_key()

	def generate_key_pair(self):
		self.key_pair = RSA.generate(2048)

	def calculate_balance(self, chain, index):
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

	def increment_balance(self, amount):
		self.honeycomb += amount

	def decrement_balance(self, amount):
		self.honeycomb -= amount

	def add_stake(self, amount, height):
		self.stakes.append((amount, height))

	def remove_stake(self, stake):
		self.stakes.remove(stake)
