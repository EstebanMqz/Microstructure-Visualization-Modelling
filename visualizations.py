"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Lab 4 (Market Microstructure) In this laboratory OB Microstructure and its characteristics will be analyzed.      -- #
# -- script: visualizations.py : Python script with the main functionality                                                      -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_4/blob/main/visualizations.py                                           -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go #plotly
import ccxt #Criptocurrencies
import time 
import plotly.express as px
from data import *


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)

def cctx_download(lvls, cripto, exchange):
    """
    Function that returns prices and quantities of given levels (as integer) Bids & Asks in an Orderbook
    for the specified criptocurrency ('BTC/USDT','ETH/USDT','XRP/USDT', or others) and
    from the following exchanges: binance, ftx or ascendex (as string).

        Parameters:
        ----------
        lvls: Levels of bids/asks in the Order Book (int).
        cripto: Criptocurrency downloadable ticker (str).
        exchanges: Criptocurrency downloadable Exchange (str).

        Returns:
        -------
        levels_ob_bid: Prices and Quantities of Bids (pos [0]) and Asks (pos [1]) as dataframes.
    """
    #Cols
    cols_ohlcv = ['exchange','timestamp', 'open', 'high', 'low', 'close', 'volume']
    #Lists to fill
    ohlcv_df = []

    if exchange == 'binance':
        binance = ccxt.binance()
        levels_ob = binance.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        timestamp = binance.iso8601(binance.milliseconds()) 
        ohlcv = binance.fetch_ohlcv(cripto, limit=25)
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'

    elif exchange == 'ftx':
        ftx = ccxt.ftx()
        levels_ob = ftx.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        timestamp = ftx.iso8601(ftx.milliseconds())
        ohlcv = ftx.fetch_ohlcv(cripto, limit=25)
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl' 
    
    elif exchange == 'bytetrade':
        bytetrade = ccxt.bytetrade()
        levels_ob = bytetrade.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        timestamp = bytetrade.iso8601(bytetrade.milliseconds())
        ohlcv = bytetrade.fetch_ohlcv(cripto, limit=25)
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'

    #OHLCV
    Op = ohlcv[0][1]
    Hi = ohlcv[0][2]
    Lo = ohlcv[0][3]
    Cl = ohlcv[0][4]
    Vol = ohlcv[0][5]
    #Append OHLCV data to df.
    ohlcv_df.append([exchange, timestamp, Op, Hi, Lo, Cl, Vol])
    ohlcv = pd.DataFrame(ohlcv_df, columns = cols_ohlcv[0:])
    ohlcv.index.name = 'OHLCV'    

    return levels_ob_bid, levels_ob_ask, ohlcv


def OBLvls_hist(lvls, cripto, exchange):
    """
    Function that plots an horizontal histogram in plotly for CriptoCurrencies OB/

        Parameters
        ----------
        lvls: Levels of bids/asks in the Order Book (int).
        cripto: Criptocurrency downloadable ticker (str).
        exchanges: Criptocurrency downloadable Exchange (str).

        x: Quantity (col) of the given cripto (str) for given lvls (int) in Order Book.
        y: Prices (col) of the given cripto (str) for given lvls (int) in Order Book.

        Returns
        -------
        Histogram of Order Book prices and quantities for n given lvls.
    """
    if exchange == 'binance':
        binance = ccxt.binance()
        levels_ob = binance.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'   

    elif exchange == 'ftx':
        ftx = ccxt.ftx()
        levels_ob = ftx.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity']) 
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'  

    elif exchange == 'bytetrade':
        bytetrade = ccxt.bytetrade()
        levels_ob = bytetrade.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity']) 
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'      

    bid = levels_ob['bids'][0][0] if len (levels_ob['bids']) > 0 else None #ToB
    ask = levels_ob['asks'][0][0] if len (levels_ob['asks']) > 0 else None #ToB
    mid = (bid+ask)*.5

    fig = go.Figure(layout_xaxis_range=[0,10])
    fig.add_trace(go.Bar(
        y= np.array(levels_ob_ask.price.astype(str)),
        x= levels_ob_ask.quantity,
        orientation='h',
    ))

    fig.add_trace(go.Bar(
        y= np.array(levels_ob_bid.price.astype(str)),
        x= levels_ob_bid.quantity,
        orientation='h',
    ))
    fig.update_layout(title_text="OB Asks vs Bids. Mid-Price: " + 
    str(round(mid,6)) + str (', ') + str(exchange) + str (': ') + str(cripto),
                    title_font_size=15,)     

    return fig.show()


def Micro(lvls, cripto, exchange, n):
    """
    Function that returns Microstructure OB and OHLCV for i levels (as integer) n times 
    from specified criptocurrency ('BTC/USDT','ETH/USDT','XRP/USDT', or others) and the 
    following exchanges: binance, ftx or bytetrade (as string).

    Parameters:
    ----------
    lvls: Levels of bids/asks in the Order Book (int).
    cripto: Criptocurrency downloadable ticker (str).
    exchanges: Criptocurrency downloadable Exchange (str).
    n: Data retrieval per exchange (int).

    Returns:
    -------
    Micro[0]: Order Books Data.
    Micro[1]: OHLCV Data.
    """
    #Cols
    cols_ob = ['exchange', 'timestamp', 'level', 'ask_volume', 'bid_volume', 'total_volume', 'mid_price', 'vwap']
    cols_ohlcv = ['exchange','timestamp', 'open', 'high', 'low', 'close', 'volume']
    #Lists to fill
    ob_df = [] 
    ohlcv_df = []

    for i in range(n):
        if exchange == 'binance':
            binance = ccxt.binance()
            levels_ob = binance.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = binance.iso8601(binance.milliseconds())
            ohlcv = binance.fetch_ohlcv(cripto, limit=1)
        
        elif exchange == 'ftx':
            ftx = ccxt.ftx()
            levels_ob = ftx.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = ftx.iso8601(ftx.milliseconds())
            ohlcv = ftx.fetch_ohlcv(cripto, limit=1)

        elif exchange == 'bytetrade':
            bytetrade = ccxt.bytetrade()
            levels_ob = bytetrade.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = bytetrade.iso8601(bytetrade.milliseconds())
            ohlcv = bytetrade.fetch_ohlcv(cripto, limit=1)

        #Order Book
        bids = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity'])
        asks = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        levels = asks.count()[0]
        ask_volume = asks.quantity.sum()
        bid_volume = bids.quantity.sum()
        total_volume = bid_volume + ask_volume
        mid_price = (bids.price[0] + asks.price[0])*.5
        vwap = bids.price[0] + asks.price[0] / (bid_volume + ask_volume)
        #OHLCV
        Op = ohlcv[0][1]
        Hi = ohlcv[0][2]
        Lo = ohlcv[0][3]
        Cl = ohlcv[0][4]
        Vol = ohlcv[0][5]

        #Append Order Book data to df.
        ob_df.append([exchange, timestamp, levels, ask_volume, bid_volume, total_volume, mid_price, vwap])
        df1 = pd.DataFrame(ob_df, columns = cols_ob)
        df1.index.name = 'Order_Books'

        #Append OHLCV data to df.
        ohlcv_df.append([exchange, timestamp, Op, Hi, Lo, Cl, Vol])
        df2 = pd.DataFrame(ohlcv_df, columns = cols_ohlcv)
        df2.index.name = 'OHLCV'
        #timestamp = binance.iso8601(binance.milliseconds())
        #df2['timestamp'] = timestamp
        time.sleep(1)

    df1['timestamp'] = [df1['timestamp'][i].strip('Z') for i in range(0, len(df1))]
    df2['timestamp'] = [df2['timestamp'][i].strip('Z') for i in range(0, len(df2))]
            
    return df1,df2


def verif_ex1(lvls, cripto, exchange, n):
    """
    Function that returns Verif 1 for i levels (as integer) n times 
    from specified criptocurrency ('BTC/USDT','ETH/USDT','XRP/USDT', or others) and the 
    following exchanges: binance, ftx or bytetrade (as string).

    Parameters:
    ----------
    lvls: Levels of bids/asks in the Order Book (int).
    cripto: Criptocurrency downloadable ticker (str).
    exchanges: Criptocurrency downloadable Exchange (str).
    n: Data retrieval per exchange (int).

    Returns:
    -------
    df1 = Section 1 Verification.
    df2 = OHLCV.
    """
    
    #Cols
    cols_verif = ['exchange', 'timestamp', 'ask', 'bid', 'ask_volume', 'bid_volume', 'spread', 'close_price']
    cols_ohlcv = ['exchange','timestamp', 'open', 'high', 'low', 'close', 'volume']
    #Lists to fill
    verif_df = []
    ohlcv_df = [] 

    for i in range(n):
        if exchange == 'binance':
            binance = ccxt.binance()
            levels_ob = binance.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = binance.iso8601(binance.milliseconds())
            ohlcv = binance.fetch_ohlcv(cripto, limit=1)
        
        elif exchange == 'ftx':
            ftx = ccxt.ftx()
            levels_ob = ftx.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = ftx.iso8601(ftx.milliseconds())
            ohlcv = ftx.fetch_ohlcv(cripto, limit=1)

        elif exchange == 'bytetrade':
            bytetrade = ccxt.bytetrade()
            levels_ob = bytetrade.fetch_order_book(cripto, limit=lvls) #Order Books 
            timestamp = bytetrade.iso8601(bytetrade.milliseconds())
            ohlcv = bytetrade.fetch_ohlcv(cripto, limit=1)

        #Verification data
        bids = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity'])
        asks = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity'])
        ask = levels_ob['asks'][0][0] if len (levels_ob['asks']) > 0 else None
        bid = levels_ob['bids'][0][0] if len (levels_ob['bids']) > 0 else None
        ask_volume = asks.quantity.sum()
        bid_volume = bids.quantity.sum()
        spread = (ask - bid) if (bid and ask) else None
        close_price = ohlcv[0][4]

        #OHLCV
        Op = ohlcv[0][1]
        Hi = ohlcv[0][2]
        Lo = ohlcv[0][3]
        Cl = ohlcv[0][4]
        Vol = ohlcv[0][5]

        #Append Verification data to verif_df.
        verif_df.append([exchange, timestamp, ask, bid, ask_volume, bid_volume, spread, close_price])
        df1 = pd.DataFrame(verif_df, columns = cols_verif)
        df1.index.name = 'Verification 1'

        #Append OHLCV data to df.
        ohlcv_df.append([exchange, timestamp, Op, Hi, Lo, Cl, Vol])
        df2 = pd.DataFrame(ohlcv_df, columns = cols_ohlcv)
        df2.index.name = 'OHLCV'

        time.sleep(1)
        df2['timestamp'] = [df2['timestamp'][i].strip('Z') for i in range(0, len(df2))]

    df1['timestamp'] = [df1['timestamp'][i].strip('Z') for i in range(0, len(df1))]
    df2['timestamp'] = [df2['timestamp'][i].strip('Z') for i in range(0, len(df2))]
            
    return df1,df2


    

    
