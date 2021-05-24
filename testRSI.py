# https://medium.com/geekculture/algorithmic-trading-in-python-rsi-e33d5e167d8a

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# RSI = 100 - 100/(1 + Avg Gain/Avg Loss)
# Using n = 14 days

def RSI(data, window=14, adjust=False):
    delta = data['Adj Close'].diff(1).dropna()
    loss = delta.copy()
    gains = delta.copy()

    gains[gains<0] = 0
    loss[loss>0] = 0

    gain_ewm = gains.ewm(com=window-1, adjust=adjust).mean()
    loss_ewm = abs(loss.ewm(com=window-1, adjust=adjust).mean())

    RS = gain_ewm / loss_ewm
    RSI = 100 - 100/(1 + RS)
    
    return RSI


spy = yf.download('SPY')
spy.head()


rsi = RSI(spy)

fig, ax = plt.subplots(2, 1, figsize=(15, 6))
ax[0].plot(spy['Adj Close'][-500:], label='Price')
ax[1].plot(rsi[-500:], label='RSI', c='purple')
ax[1].axhline(y=70, c='blue', label='Overbought')
ax[1].axhline(y=30, c='orange', label='Oversold')
ax[0].legend()
ax[1].legend(loc='lower right', fontsize=8)

spy = spy[1:]
spy['RSI'] = rsi
spy['sell_points'] = np.where((rsi > 70) & (rsi.shift(1) <= 70), 1, 0)
spy['buy_points'] = np.where((rsi < 30) & (rsi.shift(1) >= 30), 1, 0)


fig, ax = plt.subplots(2, 1, figsize=(15, 6))
ax[0].plot(spy['Adj Close'][-500:], label='Price')
ax[1].plot(rsi[-500:], label='RSI', c='purple')
ax[1].axhline(y=70, c='blue', label='Overbought')
ax[1].axhline(y=30, c='orange', label='Oversold')
ax[0].legend()
ax[1].legend(loc='lower right', fontsize=8)

ax[1].scatter(spy[spy['buy_points'] == 1][-5:].index, 
              spy[spy['buy_points'] == 1]['RSI'][-5:],
             c = 'green')

ax[1].scatter(spy[spy['sell_points'] == 1][-16:].index, 
              spy[spy['sell_points'] == 1]['RSI'][-16:],
              c = 'red')
