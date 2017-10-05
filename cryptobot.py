from flask import Flask, jsonify
from bittrex import Bittrex

app = Flask(__name__)
bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')


@app.route('/')
def home():
    return 'Home'

@app.route('/markets')
def markets():
    markets = bit.get_market_history('BTC-LTC',100)
    return jsonify(markets)

@app.route('/ticker')
def ticker():
    ticker = bit.get_ticker('BTC-LTC')
    return jsonify(ticker)


if __name__ == '__main__':
    app.run(debug=True)
