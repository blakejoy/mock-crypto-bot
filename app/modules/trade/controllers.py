from flask import Blueprint, render_template, request, g, Response
from flask_login import login_required

from app import bit

trade_module = Blueprint('trade', __name__, url_prefix='/trade')


@trade_module.route('/',methods=['GET'])
@login_required
def new_trade():
    return render_template('trade/index.html')


# TODO: implement the ticker function once the bot has started
@trade_module.route('/run',methods=['GET','POST'])
def start_bot():

    first_currency = request.form.get('time_delay')
    ticker_data = bit.get_ticker('USDT-BTC')
    return Response()

