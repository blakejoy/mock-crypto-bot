import datetime
import numpy
from flask import Blueprint, render_template, request, g, Response, jsonify
from flask_login import login_required, current_user

from app import bit
from app.modules.trade.controllers import convert_currency

bot_module = Blueprint('bot', __name__, url_prefix='/bot')

prices = []
currentMovingAvg = 0
lengthOfMA = 0

@bot_module.route('/',methods=['GET'])
@login_required
def new_trade():
    return render_template('bot/index.html')



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

    if first_currency == 'USD':
        first_currency = 'USDT'

    if second_currency == 'USD':
        second_currency = 'USDT'

    market = first_currency + '-' + second_currency

    if buy_strategy == 'Bollinger Bands':
        band_limit = bollinger_bands(market,request.form.get('high_band'),request.form.get('low_band'))



    ticker = bit.get_ticker('USDT-BTC')

    json = {'band_limit': band_limit,'ask': ticker['result']['Ask']}

    #TODO: Perform check for values
    # if  json['ask'] >= json['band_limit']['high']:
    #     return 'sell'
    # elif json['ask'] <= json['band_limit']['low']:
    #     return 'buy'
    # else:
    #     return 'keep running bot'

    return jsonify(json)


@bot_module.route('/check-balance',methods=['POST'])
def check_acct_balance():
    currency = request.form.get('currency')
    currencyDict = []


    if currency == 'USD':
        usd = format(current_user.wallet.usd_balance, '.2f')
        currencyDict.append(usd)
    elif currency == 'BTC':
        btc = format(current_user.wallet.btc_balance, '.2f')
        currencyDict.append(btc)
    elif currency == 'LTC':
        ltc = format(current_user.wallet.ltc_balance, '.2f')
        currencyDict.append(ltc)
    elif currency == 'ETH':
        eth = format(current_user.wallet.eth_balance, '.2f')
        currencyDict.append(eth)

    return jsonify(currencyDict)


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

#TODO: Check math for this strategy
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
    period_prices = prices[635:-1]

    sma = sum(period_prices)/20 #middle band

    s_deviation = numpy.std(period_prices) #standard deviation


    upper_band = sma + (s_deviation * 2) #upper band
    lower_band = sma - (s_deviation * 2) #lower band

    high_price = upper_band + (upper_band * (int(high)/100))
    low_price = lower_band - (lower_band * (int(low)/100))

    return {'high': high_price,'low': low_price}


