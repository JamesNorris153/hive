from Crypto.PublicKey import RSA
from Crypto import Random

class Bee:
	def __init__(self, name, honeycomb):
		self.name = name
		self.honeycomb = honeycomb
		self.key_pair = RSA.generate(1024, Random.new().read)
