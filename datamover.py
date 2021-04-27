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


# %%
class DataMover:
    start = ""
    stop = ""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def load_data(self, ticker):
        df = yf.download('AAPL', self.start, self.stop)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        return df[['Date', 'Close']]

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
        plt.figure(figsize=(17,5))
        plt.plot(df)
        plt.plot(df.rolling(window = 12).mean().dropna(), color='g')
        plt.plot(df.rolling(window = 12).std().dropna(), color='blue')
        plt.title('Rolling mean')
        plt.legend(['item_cnt_month', 'mean', 'std'])
     
# %%
