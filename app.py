#app.py
from models.blockchain import blockchain

def run():
	hive = blockchain()

	hive.add_new_transaction("Hello")
	hive.add_new_transaction("Wassup")
	hive.add_new_transaction("Bye")
	hive.add_new_transaction("Mmmmk bye")

	hive.mine()

	hive.add_new_transaction("awesome")
	hive.add_new_transaction("sick")

	hive.mine()

	for honeycomb in hive.chain:
		print(honeycomb.transactions)

run()
