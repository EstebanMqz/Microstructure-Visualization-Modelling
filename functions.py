
"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Lab 4 (Market Microstructure) In this laboratory OB Microstructure and its characteristics will be analyzed.      -- #
# -- script: functions.py : Python script with the main functionality                                                           -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_4/blob/main/functions.py                                                -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""

from dataclasses import dataclass
import pandas as pd
import pandas_datareader as pdr
from lib2to3.pgen2.grammar import opmap_raw
import numpy as np
from data import *

def f_leer_archivo(param_archivo):
    """
    Function that reads csv files and returns a dataframe of its content.

        Parameters
        ----------
        param_archivo: csv data.
        Returns
        -------
        data: pd.DataFrame(param_archivo)
    """

    df = pd.read_csv(param_archivo)
    return df



