from flask import Flask, jsonify, render_template, request
from bittrex import Bittrex

app = Flask(__name__)
bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')


@app.route('/')
def home():
    markets = bit.get_markets()
    return render_template('index.html',markets=markets['result'])

@app.route('/markets')
def markets(coin):
    markets = jsonify(bit.get_market_history(coin,100))
    return render_template('markets.html',markets)

@app.route('/markets/search',methods=['POST'])
def search_markets():
    markets = bit.get_market_history(request.form['market'],100)
    return jsonify(markets)


@app.route('/ticker')
def ticker():
    ticker = bit.get_ticker('BTC-LTC')
    return jsonify(ticker)


if __name__ == '__main__':
    app.run(debug=True)
