import json
import requests

from flask import Flask, request, Response
from pprint import pprint

app = Flask(__name__)

#TODO: change /<symbol> to get request parameter
@app.route("/prices/<symbol>")
def prices(symbol):

	#get rid of this and make it another route instead
	sym = findSymbol(symbol)
	if sym is not None:
		symbol = sym
	####
	
	url = "https://www.quandl.com/api/v3/datasets/WIKI/" + symbol + ".json"

	data = requests.get(url)
	data = json.loads(data.text)

	if not 'quandl_error' in data:
		resp = Response(response=json.dumps(data),
			status=200,mimetype="application/json")
	else:
		resp = Response(response=json.dumps({'error': 'Invalid symbol ' + symbol}),
			status=401,mimetype="application/json")

	return resp

@app.route("/symbol/")
def findSymbol(name):
	url = 'http://dev.markitondemand.com/Api/v2/Lookup/json?Input=' + name

	data = requests.get(url)
	data = json.loads(data.text)

	if len(data) != 0 and not 'Message' in data[0]:
		symbol = data[0]['Symbol']
	else:
		symbol = None

	return symbol


app.run(debug=True)

