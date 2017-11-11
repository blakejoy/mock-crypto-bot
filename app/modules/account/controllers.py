from flask import Blueprint, render_template
from flask_login import login_required

acct_module = Blueprint('account', __name__, url_prefix='/account')

@acct_module.route('/')
@login_required
def accountInfo():
    return render_template('index.html')

