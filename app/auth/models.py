


class Account(UserMixin, db.Model):

    __tablename__ = 'accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    firebase_user_id = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    name = db.Column(db.Text)
    photo_url = db.Column(db.Text)