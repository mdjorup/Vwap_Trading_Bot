# Algorithmic trading bot

import config
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi

class Bot:

    bar_columns=["time", "stock", "close", "volume"]

    bar_threads = ["SPY"]

    start_trading = pd.to_datetime("9:40")
    end_trading = pd.to_datetime("16:00")

    def __init__(self):
        self.api = tradeapi.REST(config.API_KEY, config.API_SECRET_KEY, config.API_BASE_URL, api_version='v2')
        self.bar_data = pd.DataFrame(columns=Bot.bar_columns)
        self.vwaps = [0,0]
        self.closes = [0,0]
        self.open_position = False

    def transmit_data(self, time, stock, close, volume):
        df2 = pd.DataFrame([[pd.to_datetime(time, utc=True), stock, close, volume]], columns=Bot.bar_columns).set_index("time")
        
        #Append and filter time
        self.bar_data = self.bar_data.append(df2).between_time('13:30', '20:00')

        #only get last 5 datapoints
        if len(self.bar_data) > 5:
            self.bar_data = self.bar_data.iloc[-5:,:]

        self.vwaps[0] = self.vwaps[1]
        self.vwaps[1] = Bot.calc_vwap(self.bar_data)
        self.closes[0] = self.closes[1]
        self.closes[1] = close

        if len(self.bar_data) < 5:
            return
        
        indicator = self.get_trade_indicator()


        if Bot.trade_conditions():
            if indicator == 0:
                return
            elif indicator == 1 and self.open_position == False:
                self.buy()
            elif indicator == -1 and self.open_position == True:
                self.sell()
        else:
            return

    def buy(self):
        self.api.submit_order(
            symbol="SPY",
            side='buy',
            type='market',
            qty='100',
            time_in_force='day',
        )
        print("Order to buy submitted at:  ", pd.to_datetime("today"))
        self.open_position = True
        return
        
    def sell(self):
        self.api.submit_order(
            symbol="SPY",
            side='sell',
            type='market',
            qty='100',
            time_in_force='day',
        )
        print("Order to sell submitted at: ", pd.to_datetime("today"))
        self.open_position = False
        return

    def trade_conditions():
        today = pd.to_datetime("today")
        if today >= Bot.start_trading and today < Bot.end_trading:
            return True
        else:
            return False

    def calc_vwap(data):
        close = data['close'].to_numpy()
        volume = data['volume'].to_numpy()
        ret_val = np.sum(close * volume) / np.sum(volume)
        return ret_val

    def get_trade_indicator(self):
        if len(self.bar_data.between_time("19:59", "20:00")) > 0:
            return -1
        elif (self.closes[1] >= self.vwaps[1]) & (self.closes[0] <= self.vwaps[0]):
            return -1
        elif (self.closes[1] <= self.vwaps[1]) & (self.closes[0] >= self.vwaps[0]):
            return 1
        else:
            return 0
