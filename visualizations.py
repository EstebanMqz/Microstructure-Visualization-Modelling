
"""
# -- ---------------------------------------------------------------------------------------------------------      -- #
# -- project: Lab 3 (Behavioral Finance) is a project that has tools to analyze the performance of trade history.   -- #
# -- script: visualizations.py : Python script with the main functionality                                          -- #
# -- author: EstebanMqz                                                                                             -- #
# -- license: GNU General Public License v3.0                                                                       -- #
# -- repository:  https://github.com/EstebanMqz/MyST_LAB_3_E3                                                       -- #
# -- ---------------------------------------------------------------------------------------------------------      -- #
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go #plotly
import plotly.express as px
from data import *


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def hist_csv(df, title, tickers, weights):
    """
    Function that returns histogram of tickers and weights of portfolio in a df.

        Parameters
        ----------
        df: Tickers and Weights of stocks in a dataframe.
        title: Title of the histogram.
        tickers: Column with tickers as str.
        weights: Column with tickers as str.

        Returns
        -------
        histogram of Tickers and Weights of the portfolio in a df.
    """
    fig = px.histogram([0,1], x=df[tickers], y= df[weights], title=title, color=df[tickers])
    fig.update_xaxes(categoryorder = 'total descending')
    fig.update_layout( yaxis = dict( tickfont = dict(size=9)), xaxis_title=tickers, yaxis_title=weights)
    fig.show()



def plotly_graph(x, y, x_label, y_label, title):
    """
    Function that plots a line+marker graph with plotly.

        Parameters
        ----------
        x: index from Dataframe of selected metric to graph with plotly.
        y: Values of the selected of selected metric to graph with plotly.
        title: Title of the plot.
        x_label: Variable name in the label x.
        y_label: Variable name in the label y.

        Returns
        -------
        Returns a didactic graph with plotly of the selected metric.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers',
    name=y_label, line=dict(color='black'), marker=dict(symbol=3, color='blue')))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig.show()

    

    
