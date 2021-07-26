import requests
import config
import json
import pandas as pd

def load_bars(timeframe, start_date, end_date):
    symbols = ["F"]
    for symbol in symbols:
        filename = 'data_files/bar_files/{}/{}.txt'.format(timeframe[1:].lower(),symbol)
        f = open(filename, 'w+')
        f.write('date,open,high,low,close,volume\n')
        url = '{}/stocks/{}/bars?start={}&end={}&timeframe={}&limit={}'.format(config.API_DATA_URL, symbol, start_date, end_date, timeframe, 10000)
        r = requests.get(url, headers=config.HEADERS)
        for bar in r.json()['bars']:
            line = '{},{},{},{},{},{}\n'.format(bar['t'], bar['o'], bar['h'], bar['l'], bar['c'], bar['v'])
            f.write(line)


def load_quotes(start_date, end_date):
    symbols = ["AAPL", "F"]
    for symbol in symbols:
        filename = 'data_files/quote_files/{}.txt'.format(symbol)
        f = open(filename, 'w+')
        f.write('date,ask_price,ask_size,bid_price,bid_size\n')
        url = '{}/stocks/{}/quotes?start={}&end={}&limit={}'.format(config.API_DATA_URL, symbol, start_date, end_date, 10000)
        r = requests.get(url, headers=config.HEADERS)
        for bar in r.json()['quotes']:
            line = '{},{},{},{},{}\n'.format(bar['t'], bar['ap'], bar['as'], bar['bp'], bar['bs'])
            f.write(line)


#load_bars("1Min", "2021-06-23", "2021-06-23")
#load_quotes("2021-07-19", "2021-07-21")


