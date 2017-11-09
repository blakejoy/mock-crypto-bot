from flask import Blueprint, render_template, request

trade_module = Blueprint('trade', __name__, url_prefix='/trade')



@trade_module.route('/',methods=['GET','POST'])
def new_trade():

    if request.method == 'POST':
        if request.form['start']:
            firstCurr = request.data.get('sel1')
            print(firstCurr)
        elif request.form['stop']:
            print('stop')
    else:
        print('hi')

    return render_template('trade/index.html')

