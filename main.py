# %%
import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datamover import DataMover
from datamover import ModelPlot
import statsmodels.api as sm
from pylab import rcParams
from statsmodels.tsa.arima_model import ARIMA

# %%
# def main():
    # %%
    today = date.today().strftime("%Y-%m-%d")
    mover = DataMover("2018-01-01", today)
    ticker_list = ["AAPL", "GOOG", "MSFT", "TSLA"]
    df = mover.load_datas(ticker_list)
    mover.write_json(df, './data.json')

    # %%
    df = mover.read_json('./data.json')

    # %%
    data = pd.concat([pd.Series(df[k]) for k in df.keys()], axis=1)
    data = data.rename(columns={k : v for (k, v) in list(zip(range(5), df.keys()))})
    data['Date'] = pd.to_datetime(data['Date'], format="%Y-%m-%d")
    data.index = data['Date']

    # %%
    mplot = ModelPlot()
    mplot.decomp_plot(data['AAPL'])

    # %%
    rcParams['figure.figsize'] = 15, 16
    decomposition = sm.tsa.seasonal_decompose(data['AAPL'], model='additive', extrapolate_trend='freq', period=12)
    decomposition.plot()
    plt.show()

    # %%


# %%
if __name__ == '__main__':
    main()    
        