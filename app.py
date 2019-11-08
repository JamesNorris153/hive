#app.py
from models.blockchain import blockchain

def run():
	hive = blockchain()

	hive.add_new_transaction("Hello World!")
	hive.mine()

	for honeycomb in hive.chain:
		print(honeycomb.transactions)

run()
