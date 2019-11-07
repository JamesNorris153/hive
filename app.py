#app.py
from models.block import block

def run():
	print("suck on my balls")
	block1 = block([1, 2], 1, 1)
	print(block1.compute_hash())

run()
