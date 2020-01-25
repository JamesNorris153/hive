import json
from hashlib import sha256

class Transaction:
	def __init__(self, sender, recipient, amount, timestamp):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.timestamp = timestamp

	def new_transaction():
		return False

#https://medium.com/coinmonks/implementing-proof-of-stake-e26fa5fb8716
