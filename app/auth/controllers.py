from flask import Blueprint, request, render_template
from flask_login import UserMixin, login_user, logout_user
from .models import Account

auth = Blueprint(auth.blueprint, __name__, url_prefix='/auth')


@auth.route('/login')
def login(email):
