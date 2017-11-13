from bittrex import Bittrex
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object("config")

#initiate bittrex
bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')

# initiate database
db = SQLAlchemy(app)

#initiate bcrypt for password encryption
bcrypt = Bcrypt(app)

#initiate flask-login for user session management
login_manager = LoginManager(app)

# migration for db model changes
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



#redirects to page not found error
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


#import all models
from app.models import *

#loads the user if user already logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#called for pages where @login_required, forcing user to sign in or sign up
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))




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

from app.modules.bot.controllers import bot_module

# register blueprint
app.register_blueprint(auth_module)
app.register_blueprint(bot_module)



