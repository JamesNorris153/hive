#app.py
from flask import Flask, request, render_template, redirect
from models.Bee import Bee
from models.Block import Block
from models.Blockchain import Blockchain
from models.Transaction import Transaction

import json
import requests
import sys
import time

app = Flask(__name__)
transaction_format = ["sender", "recipient", "amount"]
peer_format = ["address"]
transactions = []
peers = set()

blockchain = Blockchain()
address = "http://127.0.0.1:" + str(sys.argv[3])
bee = Bee(address, 0)
blockchain.add_validator(bee)


@app.route("/", methods=["GET"])
def index():
	update_transactions()

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions), 200


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
	data = request.form.to_dict()

	if not data:
		data = json.loads(request.data)

	for field in transaction_format:
		if not data.get(field):
			return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Invalid transaction data"), 406

	if not data.get("timestamp"):
		data["timestamp"] = time.time()

	transaction = Transaction(sender=data["sender"], recipient=data["recipient"], amount=data["amount"], timestamp=data["timestamp"])

	valid = blockchain.verify_transaction(transaction)

	if not valid:
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Transaction sender does not have required balance"), 403

	added = blockchain.add_transaction(transaction)

	if not added:
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Transaction already recorded"), 409

	propogate_new_transaction(transaction)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Transaction recorded"), 201


@app.route("/get_chain", methods=["GET"])
def get_chain():
	chain = []

	for block in blockchain.chain:
		chain.append(block.to_dict())

	return json.dumps({"length": len(chain), "chain": chain}), 200


@app.route("/mine_pow", methods=["GET"])
def mine_pow():
	proof, new_block = blockchain.mine_pow(bee)

	if not proof and new_block:
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="No transactions to mine"), 412

	update_transactions()
	propogate_new_block(proof, new_block)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Block #{} successfully mined".format(new_block.index)), 201


@app.route("/mine_pos", methods=["GET"])
def mine_pos():
	proof, new_block = blockchain.mine_pos(bee)

	if not new_block:
		return render_template(
			"index.html",
			address=address,
			balance=get_balance(),
			transactions=transactions,
			message="No transactions to mine"), 412

	if not proof:
		return render_template(
			"index.html",
			address=address,
			balance=get_balance(),
			transactions=transactions,
			message="No transactions to mine"), 412

	update_transactions()
	propogate_new_block(proof, new_block)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Block #{} successfully mined".format(new_block.index)), 201


@app.route("/mine_pos_v2", methods=["POST"])
def mine_pos_v2():
	data = request.form.to_dict()
	proof, new_block = blockchain.mine_pos_v2(bee, data["stake"])

	if not new_block:
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="No transactions to mine"), 412

	update_transactions()
	propogate_new_block(proof, new_block)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Block #{} successfully mined".format(new_block.index)), 201


@app.route("/get_pending_transactions", methods=["GET"])
def get_pending_transactions():
	return json.dumps(blockchain.unconfirmed_transactions), 200


@app.route("/register_new_peer", methods=["POST"])
def register_new_peer():
	peer_data = request.form.to_dict()

	for field in peer_format:
		if not peer_data.get(field):
			return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Invalid node data"), 412

	peer = Bee(peer_data["address"], None)

	response = requests.get("{}/get_publickey".format(peer_data["address"]))
	public_key = response.text
	peer.public_key = public_key

	blockchain.calculate_validator_stakes(blockchain.last_block().index + 1)
	peers.add(peer)
	blockchain.add_validator(peer)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Peer succesfully added"), 201


@app.route("/add_block", methods=["POST"])
def add_block():
	data = json.loads(request.json)
	proof = data["proof"]
	block_data = json.loads(data["block"])

	transactions = []
	for t in block_data["transactions"]:
		transactions.append(Transaction(t["sender"], t["recipient"], t["amount"], t["timestamp"]))

	block = Block(index=block_data["index"], transactions=transactions, timestamp=block_data["timestamp"], previous_hash=block_data["previous_hash"], proof_type=block_data["proof_type"], validator=block_data["validator"], stake=block_data["stake"], nonce=block_data["nonce"], signature=block_data["signature"])

	if block_data["proof_type"] == "PoW":
		added = blockchain.add_pow_block(block, proof)

	if block_data["proof_type"] == "PoS":
		added = blockchain.add_pos_block(block, proof)

	if block_data["proof_type"] == "PoS2":
		added = blockchain.add_pos_block_v2(block, proof)

	if not added:
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Invalid block"), 400

	update_transactions()
	propogate_new_block(proof, block)

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Block successfully added"), 201


@app.route("/consensus", methods=["GET"])
def consensus():
	global blockchain

	longest_chain = None
	current_length = len(blockchain.chain)

	for peer in peers:
		response = requests.get("{}/get_chain".format(peer.address))
		length = response.json()["length"]
		chain = response.json()["chain"]

		peer_blockchain = Blockchain()
		peer_blockchain.parse_json(chain)
		peer_blockchain.validators = blockchain.validators

		if length > current_length and peer_blockchain.check_validity():
			current_length = length
			longest_chain = peer_blockchain.chain

	if longest_chain:
		blockchain.chain = longest_chain
		update_transactions()
		return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Blockchain updated"), 201

	return render_template("index.html", address=address, balance=get_balance(), transactions=transactions, message="Blockchain already up to date"), 409


@app.route("/get_balance", methods=["GET"])
def get_balance():
	bee.calculate_balance(blockchain.chain, blockchain.last_block().index + 1)
	return bee.honeycomb, 200


@app.route("/get_publickey", methods=["GET"])
def get_publickey():
	return str(bee.key_pair.publickey().export_key()), 200


@app.route("/get_peers", methods=["GET"])
def get_peers():
	return str(blockchain.validators), 200


def propogate_new_block(proof, block):
	for peer in peers:
		url = "{}/add_block".format(peer.address)
		data = json.dumps({"proof": str(proof), "block": json.dumps(block.to_dict(), sort_keys=True)})
		requests.post(url, json=data)


def propogate_new_transaction(transaction):
	for peer in peers:
		url = "{}/add_transaction".format(peer.address)
		data = json.dumps(transaction.__dict__)
		requests.post(url, data=data)


def update_transactions():
	global transactions

	chain, status_code = get_chain()
	chain_data = json.loads(chain)

	transactions = []
	for block in chain_data["chain"]:
		for transaction in block["transactions"]:
			transaction["block_index"] = block["index"]
			transaction["previous_hash"] = block["previous_hash"]
			transaction["validator"] = block["validator"]
			transaction["stake"] = block["stake"]
			transaction["timestamp"] = time.ctime(transaction["timestamp"])
			transactions.append(transaction)

if __name__ == "__main__":
	app.run(debug=True)
