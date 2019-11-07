#app.py
from models.blockchain import blockchain

def run():
	hive = blockchain()

	print(hive.last_block())

run()
