import sys
import requests

att_1 = "http://127.0.0.1:8010"
att_2 = "http://127.0.0.1:8011"

requests.post(att_1 + "/register_new_peer", data={"address": "http://127.0.0.1:8000"})
requests.post(att_1 + "/register_new_peer", data={"address": "http://127.0.0.1:8001"})
requests.post(att_1 + "/register_new_peer", data={"address": "http://127.0.0.1:8002"})
requests.post(att_1 + "/register_new_peer", data={"address": "http://127.0.0.1:8003"})
requests.post(att_1 + "/register_new_peer", data={"address": "http://127.0.0.1:8004"})

requests.post(att_2 + "/register_new_peer", data={"address": "http://127.0.0.1:8005"})
requests.post(att_2 + "/register_new_peer", data={"address": "http://127.0.0.1:8006"})
requests.post(att_2 + "/register_new_peer", data={"address": "http://127.0.0.1:8007"})
requests.post(att_2 + "/register_new_peer", data={"address": "http://127.0.0.1:8008"})
requests.post(att_2 + "/register_new_peer", data={"address": "http://127.0.0.1:8009"})

for i in range(10):
	transaction_data = {"sender": "http://127.0.0.1:8000",
						"recipient": att_1,
						"amount": 5}
	r = requests.post(att_1 + "/add_transaction", data=transaction_data)
	if r.status_code == 201:
		print("node {0} successfully created transaction #{1}".format(att_1))
	else:
		print("node {0} could not create transaction #{1}".format(att_1))

	transaction_data = {"sender": "http://127.0.0.1:8005",
						"recipient": att_2,
						"amount": 5}
	r = requests.post(att_2 + "/add_transaction", data=transaction_data)
	if r.status_code == 201:
		print("node {0} successfully created transaction #{1}".format(att_2))
	else:
		print("node {0} could not create transaction #{1}".format(att_2))

	r = requests.post(att_1 + "/mine_pow", data={"stake": 0})
	if r.status_code == 201:
		print("node {} successfully mined block using PoS".format(att_1))
	else:
		print("node {} could not mine block using PoS".format(att_1))

	r = requests.post(att_2 + "/mine_pow", data={"stake": 0})
	if r.status_code == 201:
		print("node {} successfully mined block using PoS".format(att_2))
	else:
		print("node {} could not mine block using PoS".format(att_2))
