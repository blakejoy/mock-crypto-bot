from flask_login._compat import unicode

from app import db


class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class User(Base):

    __tablename__ = 'user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False,
                        unique=True)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorization Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)
    first_login = db.Column(db.SmallInteger, nullable=False)

    # Other user data
    wallet_id = db.Column(db.ForeignKey('wallet.account_number'))

    #foreign key relationships
    wallet = db.relationship('Wallet',uselist=False, backref='user')

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password
        self.role = 0
        self.status = 1
        self.first_login = 0

    def __repr__(self):
        return '<User %r>' % (self.name)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Wallet(db.Model):
    __tablename__ = 'wallet'

    def __init__(self):
        self.usd_balance = 0.0
        self.eth_balance = 0.0
        self.btc_balance = 0.0
        self.ltc_balance = 0.0

    account_number = db.Column(db.Integer,primary_key=True)
    usd_balance = db.Column(db.Float(precision=2))
    btc_balance = db.Column(db.Float(precision=2))
    eth_balance = db.Column(db.Float(precision=2))
    ltc_balance = db.Column(db.Float(precision=2))
    date_opened = db.Column(db.DateTime, default=db.func.current_timestamp())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer,primary_key=True)
    wallet_id = db.Column(db.ForeignKey('wallet.account_number'))
    transaction_type = db.Column(db.ForeignKey('transaction_type.id'))
    date = db.Column(db.DateTime,  default=db.func.current_timestamp())
    amount = db.Column(db.Float)
    tx_currency = db.Column(db.Integer,db.ForeignKey('currency.id'))

    wallet = db.relationship('Wallet',backref='transactions', uselist=False)
    currency = db.relationship('Currency', backref='transactions', uselist=False)
    transactionType = db.relationship('TransactionType', backref='transactions',uselist=True)

class TransactionType(db.Model):
    __tablename__ = 'transaction_type'

    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(100))

class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))


