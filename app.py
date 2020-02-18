#app.py
from models.Blockchain import Blockchain
from models.Block import Block
from models.Transaction import Transaction
from models.Bee import Bee
from flask import Flask, request, render_template
import requests
import time
import json
import sys


transaction_format = ["sender", "recipient", "amount"]
peer_format = ["address"]
app = Flask(__name__)
blockchain = Blockchain()
address = "http://127.0.0.1:" + str(sys.argv[3])
bee = Bee(address, 0)
blockchain.add_validator(bee)
peers = set()

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html", address = address)

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
	data = request.form.to_dict()

	for field in transaction_format:
		if not data.get(field):
			return "Invalid transaction data", 404

	blockchain.add_transaction(data["sender"], data["recipient"], data["amount"], time.time());

	return "Successfully added new transaction", 201

@app.route("/get_chain", methods=["GET"])
def get_chain():
	chain = []
	for block in blockchain.chain:
		chain.append(block.to_dict())

	return json.dumps({"length": len(chain), "chain": chain}), 200

@app.route("/mine_pow", methods=["GET"])
def mine_pow():
	proof, new_block = blockchain.mine_pow()

	if not proof and new_block:
		return "No transactions to mine", 412

	print(new_block.compute_hash())
	propogate_new_block(proof, new_block)

	return "Block #{} has successfully been mined".format(new_block.index), 200


@app.route("/mine_pos", methods=["GET"])
def mine_pos():
	proof, new_block = blockchain.mine_pos(bee)

	if not proof and new_block:
		return "No transactions to mine", 412

	propogate_new_block(proof, new_block)

	return "Block #{} has successfully been mined".format(new_block.index), 200


@app.route("/get_pending_transactions", methods=["GET"])
def get_pending_transactions():
	return json.dumps(blockchain.unconfirmed_transactions), 200


@app.route("/register_new_peer", methods=["POST"])
def register_new_peer():
	peer_data = request.form.to_dict()

	for field in peer_format:
		if not peer_data.get(field):
			return "Invalid node data", 404

	peer = Bee(peer_data["address"], None)

	response = requests.get("{}/get_publickey".format(peer_data["address"]))
	public_key = response.text
	print(public_key)
	peer.public_key = public_key

	blockchain.refresh_validator_stakes()
	peers.add(peer)
	blockchain.add_validator(peer)

	return "Successfully added new peers", 200


@app.route("/add_block", methods=["POST"])
def add_block():
	data = json.loads(request.json)
	proof = data["proof"]
	block_data = json.loads(data["block"])

	transactions = []
	for t in block_data["transactions"]:
		transactions.append(Transaction(t["sender"], t["recipient"], t["amount"], t["timestamp"]))

	new_block = Block(block_data["index"], transactions, block_data["timestamp"], block_data["previous_hash"], block_data["proof_type"], block_data["nonce"])

	if block_data["proof_type"] == "PoW":
		added = blockchain.add_pow_block(new_block, proof)

	if block_data["proof_type"] == "PoS":
		print(block_data["proof_type"])
		added = blockchain.add_pos_block(new_block, proof)

	if not added:
		return "The block was discarded by the node", 400

	return "Block added to the chain", 201


@app.route("/consensus", methods=["GET"])
def consensus():
	global blockchain

	longest_chain = None
	current_length = len(blockchain.chain)

	for peer in peers:
		response = request.get("{}/get_chain".format(peer))
		length = response.json()["length"]
		chain = response.json()["chain"]

		if length > current_length and blockchain.check_validity(chain):
			current_length = length
			longest_chain = chain

	if longest_chain:
		blockchain = longest_chain
		return True

	return False


@app.route("/balance", methods=["GET"])
def balance():
	bee.calculate_balance(blockchain.chain)
	return "Your balance is {}".format(bee.honeycomb), 200


@app.route("/get_publickey", methods=["GET"])
def get_publickey():
	print(str(bee.key_pair.publickey().export_key()))
	return str(bee.key_pair.publickey().export_key()), 200


def propogate_new_block(proof, block):
	for peer in peers:
		url = "{}/add_block".format(peer.address)
		data = json.dumps({"proof": str(proof), "block": json.dumps(block.to_dict(), sort_keys=True)})
		requests.post(url, json=data)


def propogate_new_transaction(proof, transaction):
	for peer in peers:
		url = "{}/add_transaction".format(peer.address)
		data = json.dumps(transaction.to_dict())

if __name__ == "__main__":
	app.run(debug=True)
