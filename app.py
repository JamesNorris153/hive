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
transaction_format = ["amount", "recipient", "sender", "timestamp"]
peer_format = ["address"]
transactions = []
peers = set()
blockchain = Blockchain()
address = "http://127.0.0.1:" + str(sys.argv[3])
bee = Bee(address, 0)
bee.calculate_balance(blockchain.chain, 1)


@app.route("/", methods=["GET"])
def index():
	update_transactions()

	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions), 200


@app.route("/add_block", methods=["POST"])
def add_block():
	data = json.loads(request.json)
	block_data = json.loads(data["block"])

	transactions = []
	for transaction in block_data["transactions"]:
		transactions.append(
			Transaction(
				amount=transaction["amount"],
				recipient=transaction["recipient"],
				sender=transaction["sender"],
				timestamp=transaction["timestamp"]
			)
		)

	block = Block(
		index=block_data["index"],
		transactions=transactions,
		timestamp=block_data["timestamp"],
		previous_hash=block_data["previous_hash"],
		proof_type=block_data["proof_type"],
		validator=block_data["validator"],
		stake=block_data["stake"],
		nonce=block_data["nonce"],
		signature=block_data["signature"])

	valid = blockchain.verify_block(block, blockchain.last_block())
	if not valid:
		return render_template(
			"index.html",
			address=address,
			balance=bee.honeycomb,
			peers=peers,
			stakes=bee.get_stakes(),
			transactions=transactions,
			message="Invalid block"), 400

	blockchain.add_block(block)
	propogate_new_block(block)

	update_balance()
	update_transactions()
	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions,
		message="Block successfully added"), 201


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
	data = request.form.to_dict()
	if not data:
		data = json.loads(json.loads(request.data))
	if not data.get("timestamp"):
		data["timestamp"] = time.time()

	for field in transaction_format:
		if not data.get(field):
			return render_template(
				"index.html",
				address=address,
				balance=bee.honeycomb,
				peers=peers,
				stakes=bee.get_stakes(),
				transactions=transactions,
				message="Invalid transaction data"), 406

	transaction = Transaction(
		amount=data["amount"],
		recipient=data["recipient"],
		sender=data["sender"],
		timestamp=data["timestamp"]
	)
	valid = blockchain.verify_transaction(transaction)
	if not valid:
		return render_template(
			"index.html",
			address=address,
			balance=bee.honeycomb,
			peers=peers,
			stakes=bee.get_stakes(),
			transactions=transactions,
			message="Transaction is not valid"), 403

	added = blockchain.add_transaction(transaction)
	if not added:
		return render_template(
			"index.html",
			address=address,
			balance=bee.honeycomb,
			peers=peers,
			stakes=bee.get_stakes(),
			transactions=transactions,
			message="Transaction has already been recorded"), 200

	propogate_new_transaction(transaction)
	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions,
		message="Transaction recorded"), 201


@app.route("/consensus", methods=["GET"])
def consensus():
	global blockchain

	best_chain = None
	current_stake = blockchain.stake
	current_length = len(blockchain.chain)

	for peer in peers:
		response = requests.get("{}/get_chain".format(peer))
		chain = response.json()["chain"]

		peer_blockchain = Blockchain()
		peer_blockchain.parse_json(chain)

		if not peer_blockchain.verify_chain():
			continue

		length = len(peer_blockchain.chain)
		stake = peer_blockchain.stake

		if length > current_length:
			current_length = length
			current_stake = stake
			best_chain = peer_blockchain.chain
		elif length == current_length and stake > current_stake:
			current_length = lentgh
			current_stake = stake
			best_chain = peer_blockchain.chain

	if best_chain:
		blockchain.chain = best_chain
		update_transactions()
		return render_template(
			"index.html",
			address=address,
			balance=bee.honeycomb,
			peers=peers,
			stakes=bee.get_stakes(),
			transactions=transactions,
			message="Blockchain updated"), 201

	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions,
		message="Blockchain already up to date"), 409


@app.route("/get_chain", methods=["GET"])
def get_chain():
	chain = []
	for block in blockchain.chain:
		chain.append(block.to_dict())
	return json.dumps({"chain": chain}), 200


@app.route("/mine_block", methods=["POST"])
def mine_block():
	data = request.form.to_dict()
	new_block = blockchain.mine_block(bee.address, data["proof_type"], int(data["stake"]))
	if not new_block:
		return render_template(
			"index.html",
			address=address,
			balance=bee.honeycomb,
			peers=peers,
			stakes=bee.get_stakes(),
			transactions=transactions,
			message="Could not mine transactions"), 412

	blockchain.add_block(new_block)
	propogate_new_block(new_block)

	update_balance()
	update_transactions()
	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions,
		message="Block #{} successfully mined".format(new_block.index)), 201


@app.route("/register_new_peer", methods=["POST"])
def register_new_peer():
	peer_data = request.form.to_dict()

	for field in peer_format:
		if not peer_data.get(field):
			return render_template(
				"index.html",
				address=address,
				balance=bee.honeycomb,
				peers=peers,
				stakes=bee.get_stakes(),
				transactions=transactions,
				message="Invalid node data"), 412

	peer = peer_data["address"]
	peers.add(peer)

	return render_template(
		"index.html",
		address=address,
		balance=bee.honeycomb,
		peers=peers,
		stakes=bee.get_stakes(),
		transactions=transactions,
		message="Peer succesfully added"), 201


def propogate_new_block(block):
	for peer in peers:
		url = "{}/add_block".format(peer)
		data = json.dumps({"block": json.dumps(block.to_dict(), sort_keys=True)})
		requests.post(url, json=data)

def propogate_new_transaction(transaction):
	for peer in peers:
		url = "{}/add_transaction".format(peer)
		data = json.dumps(transaction.__dict__)
		requests.post(url, json=data)

def update_balance():
	bee.calculate_balance(blockchain.chain, blockchain.last_block().index + 1)

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
	app.run(host="192.168.1.54", debug=True)
