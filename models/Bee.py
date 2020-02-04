from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, address, honeycomb, stake):
		self.address = address
		self.honeycomb = honeycomb
		self.stake = stake
		self.key_pair = None

	def generate_key_pair(self):
		self.key_pair = RSA.generate(1024, Random.new().read)

	def calculate_balance(self, blockchain):
		self.honeycomb == 0
		self.stake == 0
		
		for block in blockchain.chain:
			for transaction in transactions:
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
		self.honeycomb -= amount
