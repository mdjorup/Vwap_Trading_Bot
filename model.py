import numpy as np
import pandas as pd

###Functions
def log_returns(list_prices):
    return np.log(list_prices).diff().fillna(0)



def vwap(df, periods):
    df['vwap_{}'.format(periods)] = df.iloc[:,3:4].rolling(periods).sum(df['volume'] * df['close'])
    return
# we are going to use 60 minutes of data to try to predict the returns of the next 10 minutes

df = pd.read_csv("C:/Users/Student/Analytics Projects/AlpacaStream/data_files/bar_files/min/AAPL.txt", header=0)

df["date"] = pd.to_datetime(df["date"], utc=True)
df = df.set_index("date")
market_time = df.between_time('13:30', '20:00')
market_time['log_returns'] = log_returns(market_time['close'])
#market_time['vwap_10'] = vwap(market_time['close'], market_time['volume'], 10)
vwap(market_time, 5)


market_time.head()