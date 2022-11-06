"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Lab 4 (Market Microstructure) In this laboratory OB Microstructure and its characteristics will be analyzed.      -- #
# -- script: main.py : Python script with the main functionality                                                                -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_4/blob/main/main.py                                                     -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""
import chart_studio.plotly as py   # various tools (jupyter offline print)
import plotly.graph_objects as go  # plotting engine
import plotly.io as pio            # to define input-output of plots
pio.renderers.default = "browser"  # to render the plot locally in your default web browser
import functions as fn
import visualizations as vs
import data as dt
import pandas as pd
from os import path
import fire


