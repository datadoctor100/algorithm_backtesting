#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:34:11 2021

@author: operator
"""

# Import libraries
import backtrader as bt
import random
import pandas_datareader as pdr

# Initialize stocks
tickers = ['AG', 
           'BABA', 
           'CSTL', 
           'HLT', 
           'IEC', 
           'PYPL', 
           'PINS', 
           'UPLD', 
           'W', 
           'MSFT', 
           'SYK', 
           'SCCO', 
           'AAPL', 
           'GOOGL', 
           'IBM', 
           'USD', 
           'GLD', 
           'TMUS', 
           'T', 
           'CHTR', 
           'CBRE', 
           'AMZN', 
           'NFLX', 
           'TSLA',
           'PGR',
           'LULU',
           'PFE',
           'DLR',
           'TXN',
           'HPE',
           'WBA',
           'MCFE',
           'JPM',
           'CCL',
           'RCL',
           'JWN',
           'CNK',
           'AMC',
           'AAL',
           'LUV',
           'SPI']

# Develop
class strategy(bt.Strategy):
    
    def log(self, txt, dt = None):
        
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = 15)
        self.rsi = bt.indicators.RelativeStrengthIndex()

    def notify_order(self, order):
        
        if order.status in [order.Submitted, order.Accepted]:
            
            return

        if order.status in [order.Completed]:
            
            if order.isbuy():
                
                self.log(
                    'BUY executed, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            
            # Sell
            else:
            
                self.log('SELL executed, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        
        if not trade.isclosed:
            
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        self.log('Close, %.2f' % self.dataclose[0])
        print('rsi:', self.rsi[0])
        
        if self.order:
            
            return

        if not self.position:
            
            if (self.rsi[0] < 30):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(size=500)

        else:
            
            if (self.rsi[0] > 70):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=500)

# Run 
if __name__ == '__main__':
    
    # Choose one for testing
    ticker = random.choice(tickers)

    # Get
    df = pdr.get_data_yahoo(ticker, '2000-01-01', '2021-03-23')
    data = bt.feeds.PandasData(dataname = df, openinterest = None)        

    brain = bt.Cerebro()
    brain.addstrategy(strategy)
    brain.broker.setcash(10000)
    brain.adddata(data)
    print('Starting Portfolio Value: %.2f' % brain.broker.getvalue())

    brain.run()

    print('Final Portfolio Value: %.2f' % brain.broker.getvalue())

