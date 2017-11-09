# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, redirect, url_for
# Import the database object from the main app module
from flask_login import login_user, login_required, logout_user

from app import bcrypt
# Import module models (i.e. User)
from app.models import User, Wallet
# Import module forms
from .forms import LoginForm, SignupForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth_module = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods

@auth_module.route('/login', methods=['GET', 'POST'])
def login():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user)

            flash('Welcome %s' % user.name)

            return redirect(url_for('home'))

        flash('Incorrect email or password', 'error')

    return render_template("auth/login.html", form=form)


@auth_module.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = User(form.username.data,form.email.data,form.password.data)
        user.password = bcrypt.generate_password_hash(user.password)

        # TODO: Change how this is initialized. Im sure there is a cleaner way.
        wallet = Wallet()
        wallet.save_to_db()

        user.wallet_id = wallet.account_number
        user.save_to_db()
        flash('Thanks for registering')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html',form=form)




@auth_module.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




