# %%
class DataMover:

    def __init__():
        import streamlit as st
        from datetime import date
        import yfinance as yf
        from plotly import graph_objs as go
        import pandas as pd
        import matplotlib.style as style
        import matplotlib.pyplot as plt
        import seaborn as sns
        import json

    def seaborn_style():
        style.use('seaborn-darkgrid')
        sns.set_context('notebook')
        sns.set_palette('gist_heat')

    def load_data(ticker):
        df = yf.download(ticker, START, TODAY)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df

    def load_datas(ticker_list):
        stock_data = {}
        data_load_state = st.text("Load data...")
        for stock in ticker_list:
            data = load_data(stock)
            stock_data[stock] = data
        for k in stocks:
            tmp = {}
            df = stock_data[k]
            df = df[['Date', 'Close']]
            df = df.rename(columns={'Date': 'ds', 'Close': 'y'})
            # print(type(df['ds']))
            # df['ds'] = pd.to_datetime(df['ds'].apply(lambda x: x.strftime('%Y-%b-%d')))
            tmp['ds'] = df['ds'].tolist()
            # print(type(tmp['ds'][5]))
            print(tmp['ds'][:5])
            tmp['y'] = df['y'].tolist()
            train[k] = tmp
            train_df = pd.DataFrame(train)
        return train_df

    def write_json(df):
        df.to_json(r'./data.json')
    
    def read_json():
        with open("./data.json", "r") as file_ptr:
            obj = json.load(file_ptr)
        return obj
    
        