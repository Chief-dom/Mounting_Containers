# %%
from datetime import date
from datetime import datetime, timedelta
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
# from statsmodels.tsa.arima_model import ARIMA  # Depricated
from statsmodels.tsa.arima.model import ARIMA
import mplfinance as mpf


# %%
# def main():
    # %%
    today = date.today().strftime("%Y-%m-%d")
    mover = DataMover("2018-04-26", today)
    ticker_list = ["AAPL", "GOOG", "MSFT", "TSLA"]
    data = mover.load_data(ticker_list[0])
    # %%
    def datetime_range(start=None, end=None):
        span = end - start
        for i in range(span.days + 1):
            yield start + timedelta(days=i)
   
    date_index = list(datetime_range(start=datetime(2018, 4, 26), end=datetime(2021, 4, 26)))
    # %%
    data.Date = pd.to_datetime(data.Date)
    # %%
    date_index = pd.DataFrame(date_index)
    # %%
    date_index= date_index.rename(columns= {0:"dates"})
   # %%
   type(date_index)
    # %%
    data.set_index('Date', inplace=True)
    data.sort_index(inplace=True, ascending=True)
    # %%
    thin_data = pd.merge(date_index, data, how='left', left_on='dates', right_on='Date')
    # %%
    data.index = pd.DatetimeIndex(data.index.values)
    thin_data.isna().count()
    data = thin_data.fillna(0)
    data.index = pd.DatetimeIndex(data.index.values, freq='n')
    # %%
    thin_data.dropna(inplace=True)
    thin_data.rename(columns={'dates': 'Date'}, inplace=True)
    # thin_data.index = pd.DatetimeIndex(thin_data.index.values)
    # %%
    thin_data.set_index('Date', inplace=True)
    # %% 
    mpf.plot(thin_data, type='line', volume=True, style='charles')
    # %%
    data.rename(columns={'dates': 'Date'}, inplace=True)
    # %%
    data.reset_index(drop=True, inplace=True)
    data.set_index('Date', inplace=True)
    # %%
    mpf.plot(thin_data["2021-01-01": "2021-04-01"], figratio=(20,13), 
                    type='candle', mav=(20),tight_layout=True, 
                    volume=True, title='Apple sales from Jan 2021 to today',
                    style='yahoo')
    # %%
    mplot = ModelPlot()
    mplot.decomp_plot(thin_data['Close'])
    # %%

    # %%
    mplot.plot_arima(thin_data, 'Close')
    # %%
    rcParams['figure.figsize'] = 15, 10
    decomposition = sm.tsa.seasonal_decompose(thin_data['Close'], model='additive', extrapolate_trend='freq', period=12)
    decomposition.observed.plot(color='b')
    plt.show()
    # %%
    mplot.plot_raw_data(thin_data)
    # %%


# %%
if __name__ == '__main__':
    main()    
        