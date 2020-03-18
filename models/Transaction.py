import json
from hashlib import sha256

class Transaction:
	""" Stores data of a single transaction

	vars:
	amount - (integer) amount of honeycomb to be sent in the transaction
	recipient - (string) address of bee recieving money from the transaction
	sender - (string) address of bee sending money in the transaction
	timestamp - (float) time that the transaction was created)
	"""

	def __init__(self, amount, recipient, sender, timestamp):
		""" Constructs a Transaction object

		args:
		amount - (integer) amount of honeycomb to be sent in the transaction
		recipient - (string) address of bee recieving money from the transaction
		sender - (string) address of bee sending money in the transaction
		timestamp - (float) time that the transaction was created)
		"""
		self.amount = amount
		self.recipient = recipient
		self.sender = sender
		self.timestamp = timestamp
