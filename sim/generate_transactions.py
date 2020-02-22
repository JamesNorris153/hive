import sys
import requests

if len(sys.argv) == 2:
	total_transactions = int(sys.argv[1])
	total_nodes = 5
elif len(sys.argv) == 3:
	total_transactions = int(sys.argv[1])
	total_nodes = int(sys.argv[2])
else:
	total_transactions = 50
	total_nodes = 5

nodes = []

for i in range(total_nodes):
	nodes.append("http://127.0.0.1:800{}".format(i))

node_index = 0
for i in range(total_transactions):
	sender = nodes[node_index]

	node_index += 1
	if node_index == total_nodes:
		node_index = 0

	recipient = nodes[node_index]
	amount = 5

	transaction_data = {"sender": sender,
						"recipient": recipient,
						"amount": amount}

	r = requests.post(sender + "/add_transaction", data=transaction_data)

	if r.status_code == 201:
		print("node {0} successfully created transaction #{1}".format(sender, i + 1))
	else:
		print("node {0} could not create transaction #{1}".format(sender, i + 1))
