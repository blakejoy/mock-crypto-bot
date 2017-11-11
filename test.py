import datetime
import time
import sys, getopt

from bittrex import Bittrex

bit = Bittrex('e5b05612e299400ba26405c25549bbad','b3d4526a91fd4e81bb904ce6b6f4beae')

def main(argv):
    period = 5
    market = "BTC-LTC"
    prices = []
    currentMovingAverage = 0
    lengthOfMA = 0
    interval = "thirtyMin" #starts at the 11th of August

    try:
        opts, args = getopt.getopt(argv, "hp:c:n:",["period=","currency=","points="])
    except getopt.GetoptError:
        print('trading-bot.py -p <period> -c <currency pair> -n <period of moving average>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('trading-bot.py -p <period> -c <currency pair> -n <period of moving average>')
            sys.exit()
        elif opt in ("-p", "--period"):
                period = arg
        elif opt in ("-c", "--currency"):
            market = arg
        elif opt in ("-n", "--points"):
            lengthOfMA = int(arg)

    #historicalData = bit.get_historical_data(market,interval="fiveMin")

    while True:


        currentValue = bit.get_ticker(market)
        lastMarketPrice = currentValue["result"]["Last"]

        if (len(prices) > 0):
            currentMovingAverage = sum(prices) / float(len(prices))

        print("{:%m-%d-%Y %H:%M:%S}".format(datetime.datetime.now()) + " Period: %ss %s: %s Moving Average: %s" % (period,market,lastMarketPrice,currentMovingAverage) )

        prices.append(float(lastMarketPrice))
        prices = prices[-lengthOfMA:]
        time.sleep(int(period))


if __name__ == "__main__":
    main(sys.argv[1:])