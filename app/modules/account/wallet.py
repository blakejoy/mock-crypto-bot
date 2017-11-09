from app import db



class Wallet(db.Model):
    account_number = db.Column(db.Integer,primary_key=True)
    user = db.relationship('User', back_populates='wallet',uselist=False)