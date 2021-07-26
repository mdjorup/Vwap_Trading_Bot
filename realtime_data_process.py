import pandas as pd
import numpy as np
# This class is for collecting and storing real time data. May or may not be useful for model
class DataObject:

    trade_columns=["ticker", "time", "price", "size"]
    quote_columns=["ticker", "time", "bid_price", "bid_size", "ask_price", "ask_size"]
    bar_columns=["ticker", "start", "end", "volume", "vwap", "open", "high", "low", "close"]

    def __init__(self, threads):
        self.threads = threads
        self.trade_data = pd.DataFrame(columns=DataObject.trade_columns)
        self.quote_data = pd.DataFrame(columns=DataObject.quote_columns)
        self.bar_data = pd.DataFrame(columns=DataObject.bar_columns)

    
    def transmit_data(self, d):
        if d['ev'] == 'T':
            ticker = d['T']
            time = d['t']
            price = d['p']
            size = d['s']
            self.trade_data = pd.concat([self.trade_data, pd.DataFrame(np.array([[ticker, time, price, size]]), columns=DataObject.trade_columns)])
        elif d['ev'] == "Q":
            ticker = d['T']
            time = d['t']
            bid_price = d['p']
            bid_size = d['s']
            ask_price = d['P']
            ask_size = d['S']
            self.quote_data = pd.concat([self.quote_data, pd.DataFrame(np.array([[ticker, time, bid_price, bid_size, ask_price, ask_size]]), columns=DataObject.quote_columns)])
        else:
            ticker = d['T']
            start = d['s']
            end = d['e']
            volume = d['v']
            vwap = d['vw']
            open = d['o']
            high = d['h']
            low = d['l']
            close = d['c']
            self.bar_data = pd.concat([self.bar_data, pd.DataFrame(np.array([[ticker, start, end, volume, vwap, open, high, low, close]]), columns=DataObject.bar_columns)])
            print("Got data")
            