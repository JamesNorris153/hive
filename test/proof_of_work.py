import sys
import requests

nodes = []

transaction_data = {"sender": "http://127.0.0.1:8000",
					"recipient": "http://127.0.0.1:8000",
					"amount": 5}

r_tx = requests.post("http://127.0.0.1:8000" + "/add_transaction", data=transaction_data)

r_mine = requests.get("http://127.0.0.1:8000" + "/mine_pow")
print(r_mine.content)


"""
for i in range(10):
	nodes.append("http://127.0.0.1:800{}".format(i))

tx_index = 0
mine_index = 0
for i in range(100):
	miner = nodes[mine_index]

	mine_index += 1
	if mine_index == 10:
		mine_index = 0

	for i in range(100):
		sender = nodes[tx_index]

		tx_index += 1
		if tx_index == 10:
			tx_index = 0

		recipient = nodes[tx_index]
		amount = 5

		transaction_data = {"sender": sender,
							"recipient": recipient,
							"amount": amount}

		r_tx = requests.post(sender + "/add_transaction", data=transaction_data)

		if r_tx.status_code != 201:
			print("node {0} could not create transaction #{1}".format(sender, i + 1))

	r_mine = requests.get(sender + "/mine_pow")
	print(r_mine.get_data())
"""
