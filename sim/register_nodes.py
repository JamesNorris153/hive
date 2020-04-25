import sys
import requests

if len(sys.argv) == 3:
	start = int(sys.argv[1])
	finish = int(sys.argv[2])
elif len(sys.argv) == 2:
	start = 0
	finish = int(sys.argv[1])
else:
	start = 0
	finish = 5

nodes = []

for i in range(start, finish):
	new_node = "http://127.0.0.1:800{}".format(i)
	print("connecting node {}:".format(new_node))

	for node in nodes:
		r1 = requests.post(new_node + "/register_new_peer", data={"address": node})
		r2 = requests.post(node + "/register_new_peer", data={"address": new_node})

		if r1.status_code == 201:
			print("node {0} successfully registered with node {1}".format(new_node, node))
		else:
			print("node {0} could not connect with node {1}".format(new_node, node))

		if r2.status_code == 201:
			print("node {0} successfully registered with node {1}".format(node, new_node))
		else:
			print("node {0} could not connect with node {1}".format(node, new_node))

	print("finished connecting node {}\n".format(new_node))

	nodes.append(new_node)
