# %%
import streamlit as st
from datetime import date
import datetime
import yfinance as yf
from plotly import graph_objs as go
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns
import json
# from statsmodels.tsa.arima_model import ARIMA  # Depricated
from statsmodels.tsa.arima.model import ARIMA

# %%
class DataMover:
    start = ""
    stop = ""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def load_data(self, ticker):
        df = yf.download(ticker, self.start, self.stop)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def load_datas(self, ticker_list):
        train = []
        for stock in ticker_list:
            df = self.load_data(stock)
            date = df['Date']
            train.append(df['Close'])
        train_df  = pd.concat(train, axis=1)
        train_df.columns = ticker_list
        train_df.set_index(date, inplace=True)
        train_df.reset_index(inplace=True)
        return train_df

    def write_json(self, df, path):
        df.to_json(r'{}'.format(path))
    
    def read_json(self, path):
        with open(path, "r") as file_ptr:
            obj = json.load(file_ptr)
        return obj
    
class ModelPlot:

    def __init__(self):
        style.use('seaborn-darkgrid')
        sns.set_context('notebook')
        sns.set_palette('gist_heat')

    def decomp_plot(self, df):
        fig = plt.figure(figsize=(17,8))
        plt.plot(df)
        plt.plot(df.rolling(window = 12).mean().dropna(), color='g')
        plt.plot(df.rolling(window = 12).std().dropna(), color='blue')
        plt.title('Rolling mean')
        plt.legend(['Apple', 'mean', 'std'])
        st.write(fig)

    def plot_raw_data(self, data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['High'], name='Apple stock'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Low'], name='Google stock'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)   

    def plot_arima(self, df, label):
        indx = df.index
        start = indx[-20]
        end = indx[-1]

        arima_model = ARIMA(df[label][:-20], order=(2,3,2)).fit()
        pred = arima_model.predict(start, end, typ='levels')
        
        rolling_mean = df[label].rolling(window = 12).mean().dropna()
        rolling_std = df[label].rolling(window = 12).std().dropna()

        arima_model = ARIMA(rolling_mean[:-20], order=(2,3,3), dates=df.index).fit()
        pred_mean = arima_model.predict(start, end, typ='levels')

        arima_model = ARIMA(rolling_std[:-20], order=(2,3,3), dates=df.index).fit()
        pred_std = arima_model.predict(start, end, typ='levels')
        

        plt.figure(figsize=(17,8))
        plt.plot(df[label], alpha=0.5)
        plt.plot(rolling_mean, color='g', alpha=0.5)
        plt.plot(rolling_std, color='blue', alpha=0.5)

        # Predicted 
        plt.plot(pred)
        plt.plot(pred_mean, color='g')
        plt.plot(pred_std, color='b')
        plt.title('Rolling mean')
        plt.legend([label, 'mean', 'std', 'predicted'])  
# %%
