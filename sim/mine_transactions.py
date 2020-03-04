import sys
import requests

if len(sys.argv) == 2:
	node = int(sys.argv[1])
	mining_method = "PoS2"
elif len(sys.argv) == 3:
	node = int(sys.argv[1])
	mining_method = str(sys.argv[2])
else:
	node = 0
	mining_method = "PoS2"

def print_message(response):
	if response.status_code == 201:
		print("node {0} successfully mined block using {1}".format(node, mining_method))
	else:
		print("node {0} could not mine block using {1}".format(node, mining_method))

if mining_method == "PoW":
	r = requests.get("http://127.0.0.1:800{}/mine_pow".format(node))
	print_message(r)

if mining_method == "PoS":
	data = {"stake": 5}
	r = requests.post("http://127.0.0.1:800{}/mine_pos".format(node), data=data)
	print_message(r)

if mining_method == "PoS2":
	data = {"stake": 5}
	r = requests.post("http://127.0.0.1:800{}/mine_pos_v2".format(node), data=data)
	print_message(r)
