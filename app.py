#app.py
from models.blockchain import blockchain
from flask import Flask, request
import requests
import datetime
import json

format = ["author", "content"]
app = Flask(__name__)
blockchain = blockchain()
blockchain.create_genesis_block()
node_address = "http://127.0.0.1:8000"
posts = []
peers = set()

@app.route("/new_transaction", methods=["POST"])
def new_transaction():
	transaction = request.get_json()

	for field in format:
		if not transaction.get(field):
			return "Invalid transaction data", 404

	tx_data["timestamp"] = time.time()

	return "Successfully added new transaction", 201

@app.route("/get_chain", methods=["GET"])
def get_chain():
	chain = []
	for block in blockchain.chain:
		chain.append(block.__dict__)

	return json.dumps({"length": len(chain), "chain": chain}), 200

@app.route("/mine", methods=["GET"])
def mine():
	result = blockchain.mine()

	if not result:
		return "No transactions to mine", 412

	return "Block #{} has successfully been mined.".format(result), 200

@app.route("/get_pending_transactions", methods=["GET"])
def get_pending_transactions():
	return json.dumps(blockchain.unconfirmed_transactions), 200

@app.route("/register_new_peers", methods=["POST"])
def register_new_peers():
	nodes = request.get_json()
	if not nodes:
		return "Invalid data", 400

	for node in nodes:
		peers.add(node)

	return "Successfully added new peers", 200

@app.route("/add_block", methods=["POST"])
def add_block():
	block_data = request.get_json()
	new_block = Block(block_data["index"], block_data["transactions"], block_data["timestamp"], block_data["previous_hash"])

	proof = new_block.compute_hash()
	added = blockchain.add_block(block, proof)

	if not added:
		return "The block was discarded by the node", 400

	return "Block added to the chain", 201

@app.route("/submit", methods=["POST"])
def submit_transactions():
	author = request.form["author"]
	content = request.form["content"]

	json = {"author": author, "content": content}

	transaction_address = "{}/new_transaction".format(node_address)

	requests.post(transaction_adress, json=json, headers={"Content-type": "application/json"})

	return redirect("/")

def fetch_posts():
	chain_address = "{}/chain".format(node_address)
	response = request.get(chain_address)

	if response.status_code == 200:
		content = []
		chain = json.loads(response.content)
		for block in chain["chain"]:
			for transactions in block["transactions"]:
				transactions["index"] = block["index"]
				transactions["hash"] = block["previous_hash"]
				content.append(transactions)

		global posts
		posts = sorted(content, key=lambda k: k["timestamp"], reverse=True)

def consensus():
	global blockchain

	longest_chain = None
	current_length = len(blockchain)

	for peer in peers:
		response = request.get("http://{}/get_chain".format(peer))
		length = response.json()["length"]
		chain = response.json()["chain"]

		if length > current_length and blockchain.check_validity(chain):
			current_length = length
			longest_chain = chain

	if longest_chain:
		blockchain = longest_chain
		return True

	return False

def propogate_new_block():
	for peer in peers:
		url = "http://{}/add_block".format(peer)
		requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))

app.run(debug=True, port=8000)
