import sys
import requests

if len(sys.argv) != 2:
	total = 10
else:
	total = int(sys.argv[1])

nodes = []

for i in range(total):
	new_node = "http://127.0.0.1:800{}".format(i)
	print("connecting node {}:".format(new_node))

	for node in nodes:
		r1 = requests.post(new_node + "/register_new_peer", data={"address": node})
		r2 = requests.post(node + "/register_new_peer", data={"address": new_node})

		if r1.status_code == 200:
			print("node {0} successfully registered with node {1}".format(new_node, node))
		else:
			print("node {0} could not connect with node {1}".format(new_node, node))

		if r2.status_code == 200:
			print("node {0} successfully registered with node {1}".format(node, new_node))
		else:
			print("node {0} could not connect with node {1}".format(node, new_node))

	print("finished connecting node {}\n".format(new_node))

	nodes.append(new_node)
