from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request
from bittrex import Bittrex
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object("config")

bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


#import user model
from app.modules.auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
@login_required
def home():
    markets = bit.get_markets()
    return render_template('index.html', markets=markets['result'])


@app.route('/markets/search',methods=['POST'])
def search_markets():
    market = "{}-{}".format(request.form['base'],request.form['market'])
    markets = bit.get_market_history(market,100)
    return jsonify(markets)


#import module
from app.modules.auth.controllers import auth_module



# register blueprint
app.register_blueprint(auth_module)



db.create_all()
