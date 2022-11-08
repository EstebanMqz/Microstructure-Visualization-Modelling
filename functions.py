
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


def concatenate(df1,df2,df3, n):
    """
    Function that returns Microstructure Visualization for 3 different exchanges 
    and given dataframes that must contain the same cols: cols_ob, cols_ohlcv.

        Parameters:
        ----------
        df1: Order_Books or OHLCV Microstucture data for exchange 1.
        df2: Order_Books or OHLCV Microstucture data for exchange 2.
        df3: Order_Books or OHLCV Microstucture data for exchange 3.
        n: fetched OB & OHLCV data for each exchange. 

        Returns:
        -------
        df_MS: Array of authenticated exchanges avaliable in CCTX.

    """
    dfs = [df1, df2, df3]
    df_MS = pd.concat(dfs)
    df_MS.index = range(n*3)

    return df_MS
    

