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

class DataMover:
    start = ""
    stop = ""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def seaborn_style():
        style.use('seaborn-darkgrid')
        sns.set_context('notebook')
        sns.set_palette('gist_heat')

    def load_data(self, ticker):
        df = yf.download(ticker, self.start, self.stop)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df

    def load_datas(self, ticker_list):
        stock_data = {}
        data_load_state = st.text("Load data...")
        train = {}
        for stock in ticker_list:
            data = self.load_data(stock)
            stock_data[stock] = data
            # df = stock_data[stock]
            df = data[['Date', 'Close']]
            df = df.rename(columns={'Date': 'ds', 'Close': 'y'})
            tmp['ds'] = df['ds'].tolist()
            print(tmp['ds'][:5])
            tmp['y'] = df['y'].tolist()
            train[k] = tmp
            train_df = pd.DataFrame(train)
        return train_df

    def write_json(self, df):
        df.to_json(r'./data.json')
    
    def read_json():
        with open("./data.json", "r") as file_ptr:
            obj = json.load(file_ptr)
        return obj
    
        