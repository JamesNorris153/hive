import sys
import requests

if len(sys.argv) == 2:
	node = int(sys.argv[1])
	mining_method = "PoS2"
elif len(sys.argv) == 3:
	node = int(sys.argv[1])
	mining_method = str(sys.argv[2])
else:
	node = 1
	mining_method = "PoS2"

if mining_method == "PoW":
	r = requests.get("http://127.0.0.1:800{}/mine_pow".format(node))
	print_message(r)

def print_message(response):
	if response.status_code == 201:
		print("node {0} successfully mined block using {1}".format(node, mining_method))
	else:
		print("node {0} could not mine block using {1}".format(node, mining_method))
