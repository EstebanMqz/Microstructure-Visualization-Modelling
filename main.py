
"""
# -- ---------------------------------------------------------------------------------------------------------      -- #
# -- project: Lab 3 (Behavioral Finance) is a project that has tools to analyze the performance of trade history.   -- #
# -- script: main.py : Python script with the main functionality                                                    -- #
# -- author: EstebanMqz                                                                                             -- #
# -- license: GNU General Public License v3.0                                                                       -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_3_E3                                                        -- #
# -- ---------------------------------------------------------------------------------------------------------      -- #
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


df_1_tabla_c = dt.df_1_tabla_c
df_1_tabla_m = dt.df_1_tabla_m
df_1_tabla_e = dt.df_1_tabla_e

df_2_tabla_c = dt.df_2_tabla_c
df_2_tabla_m = dt.df_2_tabla_m
df_2_tabla_e = dt.df_2_tabla_e
