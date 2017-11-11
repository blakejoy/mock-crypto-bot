from flask import Blueprint, render_template, request, g, Response, jsonify
from flask_login import login_required, current_user

from app import bit

trade_module = Blueprint('trade', __name__, url_prefix='/trade')


@trade_module.route('/',methods=['GET'])
@login_required
def new_trade():
    return render_template('trade/index.html')


# TODO: implement the ticker function once the bot has started
@trade_module.route('/run',methods=['GET','POST'])
def start_bot():

    return Response()

@trade_module.route('/ping',methods=['POST'])
def ping():
    time_delay = request.form.get("time_delay")
    on_fail_delay = request.form.get("fail_delay")

    return Response('hi')


@trade_module.route('/check-balance',methods=['POST'])
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


@trade_module.route('/current-price')
def get_current_price():
    market = request.args.get('market')
    if market == 'USDT':
        return Response('Not Valid'),404
    else:
        # Get last price
        result = bit.get_ticker('USDT-' + request.args.get('market'))
        latest_price = format(result['result']['Last'],'.2f')
        return Response(latest_price)