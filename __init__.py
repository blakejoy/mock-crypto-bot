from flask import Flask, jsonify, render_template, request
from flask_firebase import FirebaseAuth
from bittrex import Bittrex

# define app name
app = Flask(__name__)

# load config file
app.config.from_object("config")

# load bittrex library
bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')

# use firebase authentication
fbAuth = FirebaseAuth(app)

from app.auth.controllers import

# register module
