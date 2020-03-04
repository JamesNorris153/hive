import sys
import requests

attacker_1 = "http://127.0.0.1:8005"
attacker_2 = "http://127.0.0.1:8006"

victim = "http://127.0.0.1:8000"

requests.post(attacker_1 + "/register_new_peer", data={"address": attacker_2})
requests.post(attacker_2 + "/register_new_peer", data={"address": attacker_1})

node_index = 0
for i in range(10):
	for i in range(10):
		sender = attacker_1
		recipient = attacker_2

		transaction_data = {"sender": sender,
							"recipient": recipient,
							"amount": 5}

		temp = attacker_2
		attacker_2 = attacker_1
		attacker_1 = temp

		r = requests.post(sender + "/add_transaction", data=transaction_data)

		if r.status_code == 201:
			print("node {0} successfully created transaction #{1}".format(sender, i + 1))
		else:
			print("node {0} could not create transaction #{1}".format(sender, i + 1))

	r = requests.post(attacker_1 + "/mine_pos", data={"stake": 5})

	if r.status_code == 201:
		print("node {} successfully mined block using PoS".format(attacker_1))
	else:
		print("node {} could not mine block using PoS".format(attacker_1))

requests.post(attacker_1 + "/register_new_peer", data={"address": victim})
requests.post(victim + "/register_new_peer", data={"address":attacker_1})
