
"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Lab 4 (Market Microstructure) In this laboratory OB Microstructure and its characteristics will be analyzed.      -- #
# -- script: functions.py : Python script with the main functionality                                                           -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_4/blob/main/functions.py                                                -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""

import pandas as pd
import pandas_datareader as pdr
import ccxt #Criptocurrencies
import logging as log
import numpy as np
from data import *


def find_exchanges(features=None, is_authenticated=False):
    """
    Function that returns avaliable cryptocurrencies exchanges in Python for CCTX module.

        Parameters:
        ----------
        features: None 
        is_authenticated: None 

        Returns:
        -------
        exchange_names: Array of authenticated exchanges avaliable in CCTX.

    """
    ccxt_features = []
    if features is not None:
        for feature in features:
            if not feature.endswith('Bundle'):
                ccxt_features.append(feature)

    exchange_names = []
    for exchange_name in ccxt.exchanges:
        if is_authenticated:
            exchange_auth = get_exchange_auth(exchange_name)

            has_auth = (exchange_auth['key'] != ''
                        and exchange_auth['secret'] != '')

            if not has_auth:
                continue

        log.debug('loading exchange: {}'.format(exchange_name))
        exchange = getattr(ccxt, exchange_name)()

        if ccxt_features is None:
            has_feature = True

        else:
            try:
                has_feature = all(
                    [exchange.has[feature] for feature in ccxt_features]
                )

            except Exception:
                has_feature = False

        if has_feature:
            try:
                log.info('initializing {}'.format(exchange_name))
                exchange_names.append(exchange_name)

            except Exception as e:
                log.warn(
                    'unable to initialize exchange {}: {}'.format(
                        exchange_name, e
                    )
                )

    return exchange_names 


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

    elif exchange == 'ascendex':
        ascendex = ccxt.ascendex()
        levels_ob = ascendex.fetch_order_book(cripto, limit=lvls) #Order Books 
        levels_ob_bid = pd.DataFrame(levels_ob['bids'], columns = ['price','quantity']) #Levels and Qt
        levels_ob_ask = pd.DataFrame(levels_ob['asks'], columns = ['price','quantity']) 
        levels_ob_bid.index.name = 'Bid_Lvl' 
        levels_ob_ask.index.name = 'Ask_Lvl'      

    return levels_ob_bid, levels_ob_ask
    

