
import urllib3
import certifi
import json
import time

''' Notes...

urllib3 - gets the info from the web
certifi - SSL certificate verification
json - to parse and decode Json


- Convert USD to Bitcoin
    bitcoin_value = current U.S. dollar price for a bitcoin * (U.S. dollar amount to spend on a bitcoin/100000000)

- Convert Bitcoin to USD
    us_dollar_value = (bitcoin amount/current U.S. dollar price for a bitcoin) * 100000000

- What does bid mean?
  This is the HIGHEST price that a trader is willing to PAY for that moment.

- What does ask mean?
    The LOWEST price someone is willing to SELL at that moment.


- How to implement stupid 1 % buying and selling strategy
    1. Get initial US dollar value for bitcoin
    2. Get initial ASK and bid price from bittrex
    3. update every 10 seconds
        if initialUSDollarValue - (.01 * initialUSDollarValue) >= CurrentUSDollarValue then
          check if there is bitcoin to sell
            if yes then sell bitcoin for cash
              subtract bitcoin from wallet
              add cash to wallet
            if no then print message

        if initialUSDollarValue - (.01 * initialUSDollarValue) <= CurrentUSDollarValue then
          check if there is cash in wallet to buy stuff
            if yes then buy the amount of bitcoin we can afford
              subtract cash from wallet
              add bitcoin to wallet
            if no print message




'''

__author__ = 'DeLander Collins Jr.'


def get_current_price(currency):
    """Request the current USD price for bitcoins data with certificate verification from coindesk API"""

    # Build coindesk url for API
    coindesk_url = 'https://api.coindesk.com/v1/bpi/currentprice/' + currency
    # print('CoinDesk Currency URL:', coindesk_url)

    # Pull current price from coinDesk
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    request_current_price = http.request('GET', coindesk_url)
    current_price_json = json.loads(request_current_price.data.decode('utf-8'))
    return current_price_json


def get_ticker(market):
    """Request the current ticker values for bitcoin using the bittrex API"""

    # Build bittrex url for API
    ticker_url = 'https://bittrex.com/api/v1.1/public/getticker?market=' + market
    # print('Bittrex ticker URL:', ticker_url)

    # Pull the ticker data with certificate verification from bittrex
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    request_market_data = http.request('GET', ticker_url)
    market_json = json.loads(request_market_data.data.decode('utf-8'))
    return market_json


def usd2btc(dollar_amount, current_us_price):
    """Convert the US dollar amount to the current bitcoin value"""
    bitcoin_value = dollar_amount/ current_us_price
    # bitcoin_value = current_us_price * (dollar_amount/100000000)
    bitcoin_value = round(bitcoin_value, 4)
    return bitcoin_value


def btc2usd(bitcoin_value, current_us_price):
    """Convert the Bitcoin value to current US dollar amount"""
    us_dollar_value = current_us_price * bitcoin_value
    us_dollar_value = round(us_dollar_value, 1)
    return us_dollar_value


'''
# Get user input to create wallet for user to hold dollars and bitcoins
# name = input("Enter your Name: ")
# cashInWallet = input("Enter your U.S. dollar deposit amount: $ ")
name = 'DeLander'
cashInWallet = 50.0
bitcoin = 0

# Create crypto currency wallet to store in json
userWallet = {'Name': name, 'Cash': cashInWallet, 'BTC': bitcoin}
print()
print('Wallet contains: NAME-', userWallet['Name'], 'CASH-', userWallet['Cash'], 'Bitcoin-', userWallet['BTC'])
print()

# Start loop here

# time.sleep(5)
currentPrice_json = get_current_price('USD')
numbers = currentPrice_json['bpi']['USD']['rate_float']
numbers = round(numbers, 2)
print('Current U.S. price $', numbers)
print()

# Convert U.S. Dollars to bitcoin estimate
BitcoinAmount = usd2btc(userWallet['Cash'], numbers)
print('Bitcoin value for $', userWallet['Cash'], 'is', BitcoinAmount)

# Convert Bitcoin estimate to U.S. Dollar estimate
DollarAmount = btc2usd(BitcoinAmount, numbers)
print('Dollar value for BTC', BitcoinAmount, 'is', DollarAmount)

# Get market ticker data
marketTicker_json = get_ticker('USDT-BTC')
print(marketTicker_json)
tickerOut = marketTicker_json['result']['Bid']
print('Current BTC Bid ', tickerOut)
print()
'''

# Get user input to create wallet for user to hold dollars and bitcoins
# name = input("Enter your Name: ")
# cashInWallet = input("Enter your U.S. dollar deposit amount: $ ")
name = 'DeLander'
cashInWallet = 15000
bitcoin = .5

# Percent change
percentChange = .0001

# Risk (high 90 %, med 40 %, low 10 %)
risk = .9

# Create crypto currency wallet to store in json
userWallet = {'Name': name, 'Cash': cashInWallet, 'BTC': bitcoin}
print('Wallet contains: NAME-', userWallet['Name'], 'CASH-', userWallet['Cash'], 'Bitcoin-', userWallet['BTC'])
print()

# Get current U.S. Dollar value for bitcoin
initialUSPrice_json = get_current_price('USD')
initialUSPrice = initialUSPrice_json['bpi']['USD']['rate_float']
initialUSPrice = round(initialUSPrice, 2)
# print('Current U.S. price $', initialUSPrice)
# print()

# Do this 100 times...for testing
for x in range(1, 100):
    print("Loop #:", x)

    # Take quick break to see if price changed
    time.sleep(5)

    # Grab current BTC US dollar price to see if it's changed
    btc_price_json = get_current_price('USD')
    btc_price = btc_price_json['bpi']['USD']['rate_float']
    btc_price = round(btc_price, 2)
    print('Current bitcoin price is:', btc_price)

    # Get Ask Price. Lowest price a trader is will to sell for at the moment
    btc_ask_price = get_ticker('USDT-BTC')
    btc_ask_price = btc_ask_price['result']['Ask']
    print('ask price:', btc_ask_price)

    # Get Bid Price. Highest price a trader is willing to pay for the moment
    btc_bid_price = get_ticker('USDT-BTC')
    btc_bid_price = btc_bid_price['result']['Bid']
    print('bid price:', btc_bid_price)

    # Set sell and buy price
    sellPrice = round(initialUSPrice + (percentChange * initialUSPrice), 2)
    buyPrice = round(initialUSPrice - (percentChange * initialUSPrice), 2)
    print("bot buy price:", buyPrice)
    print("bot sell price", sellPrice)
    print()

    # Price is up by the set percent, but you have no bitcoins to sell...
    if btc_price >= sellPrice and userWallet['BTC'] == 0:
        print("There are", userWallet['BTC'], "bitcoins in your wallet for sale. Coins will be purchased at", buyPrice)

    # Price is up by the set percent and We have bitcoins to sell!!!!
    elif btc_price >= sellPrice and userWallet['BTC'] > 0:
        coins2DollarsAmount = btc2usd(userWallet['BTC'], btc_bid_price)
        print('We can trade', userWallet['BTC'], 'bitcoins for', coins2DollarsAmount, 'dollars')

        # Update Wallet with new amount
        userWallet['Cash'] += coins2DollarsAmount
        userWallet['BTC'] = 0

        # Set new Initial price value for U.S. Dollar value for bitcoin
        initialUSPrice_json = get_current_price('USD')
        initialUSPrice = initialUSPrice_json['bpi']['USD']['rate_float']
        initialUSPrice = round(initialUSPrice, 2)
        print('New wallet amount:', 'CASH-', userWallet['Cash'], 'Bitcoin', userWallet['BTC'])
        print()

    # Price is down by set percent but we have no cash to buy
    elif btc_price <= buyPrice and userWallet['Cash'] == 0:
        coins2DollarsAmount = btc2usd(userWallet['BTC'], btc_bid_price)
        print("There are", userWallet['Cash'], "dollars in your wallet for a purchase. If coins are sold at current")
        print("rate you can make", coins2DollarsAmount)
        print()

    # Price is down by set percent and we have cash to buy!!!!
    elif btc_price <= buyPrice and userWallet['Cash'] > 0:

        # See how much we would get for our bitcoins at the current rate
        bitcoinAmount = usd2btc(userWallet['Cash'], btc_ask_price)
        print('We can trade', userWallet['Cash'] / 4, 'dollars for', bitcoinAmount / 4, 'bitcoins')

        # Update Wallet with new amount
        userWallet['Cash'] /= 4
        userWallet['BTC'] += usd2btc(userWallet['Cash'] / 4, btc_ask_price)

        # Set new Initial price value for U.S. Dollar value for bitcoin
        initialUSPrice_json = get_current_price('USD')
        initialUSPrice = initialUSPrice_json['bpi']['USD']['rate_float']
        initialUSPrice = round(initialUSPrice, 2)
        print('New wallet amount:', 'CASH-', userWallet['Cash'], 'Bitcoin', userWallet['BTC'])
        print()

print('Name:', userWallet['Name'], 'Cash', userWallet['Cash'], 'Bitcoin', userWallet['BTC'])