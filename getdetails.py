#!/usr/bin/env python
import sys
import urllib2
import json
import time
import csv
from datetime import datetime

def main():
  option = sys.argv[1]

  ##
  ##    If user input 1, it is an account, else it's a single tx
  ##
  if option == '1':
      print "here"
      account(sys.argv[2])

def account(address):
    etherscan_url = 'http://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&sort=desc'
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(etherscan_url)
    transactions = json.loads(response.read())
    file_name = address + '.csv'
    local_file = open(file_name,'a+')

    for i in range(len(transactions['result'])):
        tx_type = None
        if transactions['result'][i]['contractAddress']:
            tx_type = "Poll"
        else:
            tx_type = "Vote"
        unixtime = int(transactions['result'][i]['timeStamp'])
        # gasprice converted into Shannon/gwei
        gasprice_wei = int(transactions['result'][i]['gasPrice'])
        gasprice = gasprice_wei * 0.000000001
        gasused = int(transactions['result'][i]['gasUsed'])

        ##
        ##  Get Poloniex ETH BTC price, generate average
        ##
        interval_low = str(unixtime - 1800)
        interval_high = str(unixtime + 1800)

        poloniex_url = 'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=' + interval_low + '&end=' + interval_high + '&period=1800'

        poloniex_price_instance = opener.open(poloniex_url)
        poloniex_price = json.loads(poloniex_price_instance.read())

        eth_interval_price = 0
        for i in range(len(poloniex_price)):
            eth_interval_price += poloniex_price[i]['weightedAverage']

        eth_average = round(eth_interval_price / len(poloniex_price), 4)

        ##
        ##  Get Coinbase BTC USD price, generate average
        ##
        interval_low_coinbase = datetime.fromtimestamp(unixtime - 1800).isoformat()
        interval_high_coinbase = datetime.fromtimestamp(unixtime + 1800).isoformat()

        coinbase_url = 'https://api.exchange.coinbase.com/products/BTC-USD/candles?start=' + interval_low_coinbase + '&end=' + interval_high_coinbase + '&granularity=1800'

        coinbase_price_instance = opener.open(coinbase_url)
        coinbase_price = json.loads(coinbase_price_instance.read())

        btc_interval_price = 0
        for i in range(len(coinbase_price)):
            btc_interval_price += (coinbase_price[i][3] + coinbase_price[i][4]) / 2

        btc_average = round(btc_interval_price / len(coinbase_price))

        eth_price = round(eth_average * btc_average, 4)

        tx_cost_ether = round((gasprice * gasused) / 1000000000, 8)
        tx_cost_usd = round(tx_cost_ether * eth_price,8)

        fileWriter = csv.writer(local_file, delimiter= ',')
        fileWriter.writerow([tx_type,unixtime,gasused,gasprice,eth_price,tx_cost_ether,tx_cost_usd])
        print "Added New: " + tx_type
        time.sleep(1)

    local_file.close()

if __name__ == '__main__':
    main()
