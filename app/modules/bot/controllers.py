import datetime
from flask import Blueprint, render_template, request, g, Response, jsonify
from flask_login import login_required, current_user

from app import bit
import urllib3
import certifi
import json
import time

bot_module = Blueprint('bot', __name__, url_prefix='/bot')

prices = []
currentMovingAvg = 0
lengthOfMA = 0

@bot_module.route('/',methods=['GET'])
@login_required
def new_trade():
    return render_template('bot/index.html')

@bot_module.route('/trade-history')
@login_required
def trade_history():
    return Response('Hi')

#TODO: Implement gain strategy

@bot_module.route('/start',methods=['POST'])
def start():
    """
    Returns the data of the market based on the strategy that is chosen.
    This function initializes the bot

    :rtype: dict
    :return: the ask price of market and the high and low band percentages
    """
    first_currency = request.form.get('first_currency')
    second_currency = request.form.get('second_currency')
    buy_strategy =  request.form.get('buy_strat')
    sell_strategy = request.form.get('sell_strat')
    amount = request.form.get('amount')
    buy_level = request.form.get('buy_level')
    sell_level = request.form.get('sell_level')

    current_balance = get_wallet_currency_balance(first_currency)


    if first_currency == 'USD':
        first_currency = 'USDT'

    if second_currency == 'USD':
        second_currency = 'USDT'


    market = first_currency + '-' + second_currency
    ticker = bit.get_ticker(market)

    if buy_strategy == 'Bollinger Bands':
        band_limit = bollinger_bands(market,request.form.get('high_band'),request.form.get('low_band'))
        json = {'band_limit': band_limit,'ask': ticker['result']['Ask'], 'last_bid': ticker['result']['Bid']}
    if buy_strategy == 'Percent Gain':
        percents = percent_change(market, request.form.get('gain_buy_level'), request.form.get('gain_sell_level'))
        json = {'percents': percents, 'ask': ticker['result']['Ask'], 'last_bid': ticker['result']['Bid']}


    if sell_strategy == 'Bollinger Bands':
        band_limit = bollinger_bands(market,request.form.get('high_band'),request.form.get('low_band'))
        json = {'band_limit': band_limit,'ask': ticker['result']['Ask'], 'last_bid': ticker['result']['Bid']}
    if sell_strategy == 'Percent Gain':
        percents = percent_change(market, request.form.get('gain_buy_level'), request.form.get('gain_sell_level'))
        json = {'percents': percents, 'ask': ticker['result']['Ask'], 'last_bid': ticker['result']['Bid']}





    #TODO: Perform check for values
    # if  json['ask'] >= json['band_limit']['high']:
    #     return 'sell'
    # elif json['ask'] <= json['band_limit']['low']:
    #     return 'buy'
    # else:
    #     return 'keep running bot'

    return jsonify(json)


@bot_module.route('/check-balance',methods=['GET','POST'])
def check_acct_balance():
    currency = request.args.get('currency')

    if request.method == "GET":
        balance = get_wallet_currency_balance(currency)
    else:
        if float(request.args.get('amount')) > 0.0:
            balance = get_wallet_currency_balance(currency)
        else:
            balance = 0



    return jsonify(balance)


@bot_module.route('/current-price')
def get_current_price():
    market = request.args.get('market')
    if market == 'USDT':
        return Response('Not Valid'),404
    else:
        # Get last price
        result = bit.get_ticker('USDT-' + request.args.get('market'))
        latest_price = format(result['result']['Last'],'.2f')

        return Response(latest_price)


def get_wallet_currency_balance(currency):
    if currency == 'USD':
        amount = format(current_user.wallet.usd_balance, '.2f')
    elif currency == 'BTC':
        amount = format(current_user.wallet.btc_balance, '.2f')
    elif currency == 'LTC':
        amount = format(current_user.wallet.ltc_balance, '.2f')
    elif currency == 'ETH':
        amount = format(current_user.wallet.eth_balance, '.2f')


    return amount


def get_current_price(currency):
    """Request the current USD price for bitcoins data with certificate verification from coindesk API"""

    # Build coindesk url for API
    coindesk_url = 'https://api.coindesk.com/v1/bpi/currentprice/' + currency
    # print('CoinDesk Currency URL:', coindesk_url)

    # Pull current price from coinDesk
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    request_current_price = http.request('GET', coindesk_url)
    current_price_json = json.loads(request_current_price.data.decode('utf-8'))
    return current_price_json


def get_ticker(market):
    """Request the current ticker values for bitcoin using the bittrex API"""

    # Build bittrex url for API
    ticker_url = 'https://bittrex.com/api/v1.1/public/getticker?market=' + market
    # print('Bittrex ticker URL:', ticker_url)

    # Pull the ticker data with certificate verification from bittrex
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    request_market_data = http.request('GET', ticker_url)
    market_json = json.loads(request_market_data.data.decode('utf-8'))
    return market_json


def usd2btc(dollar_amount, current_us_price):
    """Convert the US dollar amount to the current bitcoin value"""
    bitcoin_value = dollar_amount / current_us_price
    # bitcoin_value = current_us_price * (dollar_amount/100000000)
    bitcoin_value = round(bitcoin_value, 4)
    return bitcoin_value


def btc2usd(bitcoin_value, current_us_price):
    """Convert the Bitcoin value to current US dollar amount"""
    us_dollar_value = current_us_price * bitcoin_value
    us_dollar_value = round(us_dollar_value, 1)
    return us_dollar_value


def bollinger_bands(market,high,low):
    """""
    Used to get bollinger bands high and low percentages.

    :parm market: market
    :type market: str

	:param high: integer number for percent of high
	:type high: int

	:param low: integer number for percent of low
	:type low: int

    :return: dict
    """
    prices = []

    ticks = bit.get_ticks(market,'day')

    #average of high and low for each day
    for tick in ticks['result']:
        avg_price = (tick['H'] + tick['L']) / 2
        prices.append(avg_price)

    #20 day period
    period_prices = prices[-21:-1]


    sma = sum(period_prices)/20 #middle band

    s_deviation = numpy.std(period_prices) #standard deviation


    upper_band = sma + (s_deviation * 2) #upper band
    lower_band = sma - (s_deviation * 2) #lower band

    high_price = upper_band + (upper_band * (int(high)/100))
    low_price = lower_band - (lower_band * (int(low)/100))

    return {'high': high_price,'low': low_price}


def percent_change(market, buy_level, sell_level):

    cashInWallet = current_user.wallet.usd_balance
    bitcoin = current_user.wallet.btc_balance

    # Risk (high 90 %, med 40 %, low 10 %)
    risk = .9

    # Create crypto currency wallet to store in json
    print('Wallet contains: NAME-', current_user.name, 'CASH-', cashInWallet, 'Bitcoin-', bitcoin)
    print()


    # Get current U.S. Dollar value for bitcoin

    result = bit.get_ticker('USDT-' + request.args.get('market'))
    latest_price = format(result['result']['Last'], '.2f')
    initialUSPrice = round(latest_price, 2)

    print("Initial Bitcoin Price: ", initialUSPrice)


    cashInWallet = current_user.wallet.usd_balance
    bitcoin = current_user.wallet.btc_balance

    print("Loop #:", x)

    # Take quick break to see if price changed
    time.sleep(5)

    # Grab current BTC US dollar price to see if it's changed
    result = bit.get_ticker('BTC-' + request.args.get('market'))
    latest_price = format(result['result']['Last'], '.2f')
    btc_price_json = get_current_price('USD')
    btc_price = btc_price_json['bpi']['USD']['rate_float']
    btc_price = round(btc_price, 2)
    print('Current bitcoin price is:', btc_price)

    # Get Ask Price. Lowest price a trader is will to sell for at the moment
    btc_ask_price = get_ticker('USDT-BTC')
    btc_ask_price = btc_ask_price['result']['Ask']
    print('ask price:', btc_ask_price)

    # Get Bid Price. Highest price a trader is willing to pay for the moment
    btc_bid_price = get_ticker('USDT-BTC')
    btc_bid_price = btc_bid_price['result']['Bid']
    print('bid price:', btc_bid_price)

    # Set sell and buy price
    sellPrice = round(initialUSPrice + (buy_level * initialUSPrice), 2)
    buyPrice = round(initialUSPrice - (buy_level * initialUSPrice), 2)
    print("bot buy price:", buyPrice)
    print("bot sell price", sellPrice)
    print()

    # Price is up by the set percent, but you have no bitcoins to sell...
    if btc_price >= sellPrice and current_user.wallet.btc_balance == 0:
        print("There are", current_user.wallet.btc_balance, "bitcoins in your wallet for sale. Coins will be purchased at",
              buyPrice)

    # Price is up by the set percent and We have bitcoins to sell!!!!
    elif btc_price >= sellPrice and current_user.wallet.btc_balance > 0:
        coins2DollarsAmount = btc2usd(current_user.wallet.btc_balance, btc_bid_price)
        print('We can trade', current_user.wallet.btc_balance, 'bitcoins for', coins2DollarsAmount, 'dollars')

        # Update Wallet with new amount
        cashInWallet += coins2DollarsAmount
        current_user.wallet.btc_balance = 0

        # Set new Initial price value for U.S. Dollar value for bitcoin
        initialUSPrice_json = get_current_price('USD')
        initialUSPrice = initialUSPrice_json['bpi']['USD']['rate_float']
        initialUSPrice = round(initialUSPrice, 2)
        print('New wallet amount:', 'CASH-', cashInWallet, 'Bitcoin', current_user.wallet.btc_balance)
        print()

    # Price is down by set percent but we have no cash to buy
    elif btc_price <= buyPrice and cashInWallet == 0:
        coins2DollarsAmount = btc2usd(current_user.wallet.btc_balance, btc_bid_price)
        print("There are", cashInWallet,
              "dollars in your wallet for a purchase. If coins are sold at current")
        print("rate you can make", coins2DollarsAmount)
        print()

    # Price is down by set percent and we have cash to buy!!!!
    elif btc_price <= buyPrice and cashInWallet > 0:

        # See how much we would get for our bitcoins at the current rate
        bitcoinAmount = usd2btc(cashInWallet, btc_ask_price)
        print('We can trade', cashInWallet / 4, 'dollars for', bitcoinAmount / 4, 'bitcoins')

        # Update Wallet with new amount
        cashInWallet /= 4
        current_user.wallet.btc_balance += usd2btc(cashInWallet / 4, btc_ask_price)

        # Set new Initial price value for U.S. Dollar value for bitcoin
        initialUSPrice_json = get_current_price('USD')
        initialUSPrice = initialUSPrice_json['bpi']['USD']['rate_float']
        initialUSPrice = round(initialUSPrice, 2)
        print('New wallet amount:', 'CASH-', cashInWallet, 'Bitcoin', current_user.wallet.btc_balance)
        print()

    return {'Cash': cashInWallet, 'BTC': bitcoin}