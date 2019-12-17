import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

node_address = "http://127.0.0.1:8000"

posts = []

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

@app.route('/')
def index():
	fetch_posts()
	return render_template("index.html", name="James")
