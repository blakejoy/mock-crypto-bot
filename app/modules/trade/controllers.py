from flask_login import current_user


def convert_currency(total_to_convert,conversion_price):
    converted_currency = total_to_convert/float(conversion_price)

    current_user.wallet.btc_balance+= converted_currency
    current_user.wallet.save_to_db()

