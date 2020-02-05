#app.py
from models.Blockchain import Blockchain
from models.Bee import Bee
from flask import Flask, request, render_template
import requests
import time
import json

transaction_format = ["recipient", "amount"]
peer_format = ["address"]
app = Flask(__name__)
blockchain = Blockchain()
address = "http://127.0.0.1:8001/"
bee = Bee(address, 1000, 50)
bee.generate_key_pair()
posts = []
peers = set()

@app.route("/", methods=["GET"])
def index():
	if bee.stake > 0:
		blockchain.add_validator(bee)
	return render_template("index.html")

@app.route("/new_transaction", methods=["POST"])
def new_transaction():
	data = request.form.to_dict()

	for field in transaction_format:
		if not data.get(field):
			return "Invalid transaction data", 404

	blockchain.add_transaction(bee.address, data["recipient"], data["amount"], time.time());

	return "Successfully added new transaction", 201

@app.route("/get_chain", methods=["GET"])
def get_chain():
	chain = []
	for block in blockchain.chain:
		chain.append(block.to_dict())

	return json.dumps({"length": len(chain), "chain": chain}), 200

@app.route("/mine_pow", methods=["GET"])
def mine_pow():
	result = blockchain.mine_pow()

	if not result:
		return "No transactions to mine", 412

	return "Block #{} has successfully been mined".format(result), 200

@app.route("/mine_pos", methods=["GET"])
def mine_pos():
	result = blockchain.mine_pos(bee)

	if not result:
		return "No transactions to mine", 412

	return "Block #{} has successfully been mined".format(result), 200

@app.route("/get_pending_transactions", methods=["GET"])
def get_pending_transactions():
	return json.dumps(blockchain.unconfirmed_transactions), 200

@app.route("/register_new_peer", methods=["POST"])
def register_new_peer():
	peer_data = request.form.to_dict()
	print(peer_data["address"])

	for field in peer_format:
		if not peer_data.get(field):
			return "Invalid node data", 404

	peer = Bee(peer_data["address"], None, None)
	peer.calculate_balance(blockchain)
	peers.add(peer)
	blockchain.add_validator("")

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

app.run(debug=True, port=8001)
