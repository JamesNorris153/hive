from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, address, honeycomb, stake):
		self.address = address
		self.honeycomb = honeycomb
		self.stake = stake
		self.key_pair = RSA.generate(1024, Random.new().read)
