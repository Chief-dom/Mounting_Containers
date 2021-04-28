# %%
# https://medium.com/@josemarcialportilla/using-python-and-auto-arima-to-forecast-seasonal-time-series-90877adff03c
# https://towardsdatascience.com/arima-forecasting-in-python-90d36c2246d3
# %%
import streamlit as st
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
def main():
    # %%
    style.use('seaborn-darkgrid')
    sns.set_context('notebook')
    sns.set_palette('gist_heat')
    st.set_page_config(layout='wide')
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
    date_index = pd.DataFrame(date_index)
    date_index= date_index.rename(columns= {0:"dates"})
    data.set_index('Date', inplace=True)
    data.sort_index(inplace=True, ascending=True)
    # %%
    thin_data = data.resample('2w').mean()
    # %%
    mplot = ModelPlot()
    mplot.decomp_plot(thin_data['Close'])
    chart1 = thin_data['Close']
    chart2 = thin_data['Close'].rolling(window = 12).mean().dropna()
    chart3 = thin_data['Close'].rolling(window = 12).std().dropna()
    # %%
    df = pd.concat([chart1, chart2, chart3], axis=1)
    # %%
    df.columns=['Close', 'Rolling Mean', 'Rolling Std']
    # %%
    # df
    # %%
    # st.line_chart([thin_data['Close'], thin_data['Close'].rolling(window = 12).mean().dropna()])
    st.title('Rolling value decomposition on Apple stock')
    st.line_chart(df, width=800)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.line_chart(df, width=200)
    with col2:
        st.line_chart(df, width=200)
    with col3:
        st.line_chart(df, width=200)


    # st.altair_chart([thin_data['Close'] | thin_data['Close'].rolling(window = 12).mean().dropna()])
    # %%
    mplot.plot_arima(thin_data, 'Close')
    # %%
    rcParams['figure.figsize'] = 17, 12
    decomposition = sm.tsa.seasonal_decompose(thin_data['Close'], model='additive', extrapolate_trend='freq', period=6)
    decomposition.plot()
    plt.show()
    # %%
    mpf.plot(thin_data["2020-04-01": "2021-04-01"], figratio=(17,8), 
                type='candle', mav=(20), 
                volume=True, title='Apple sales from April 2020 to April 20201')
    # %%
    mpf.plot(thin_data["2019-04-01": "2020-04-01"], figratio=(17,8), 
                type='candle', mav=(20), 
                volume=True, title='Apple sales from April 2019 to April 2020')
    
    # %%
    # mplot.plot_raw_data(thin_data)
    # %%


# %%
if __name__ == '__main__':
    main()    
        