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
def main():
    # %%
    style.use('seaborn-darkgrid')
    sns.set_context('notebook')
    sns.set_palette('gist_heat')

    START = "2018-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title("Stock Prediction App")

    stocks = ["AAPL", "GOOG", "MSFT", "TSLA"]
    selected_stock = st.selectbox("Select dataset for prediction", stocks)

    # n_years = st.slider("Years of prediction:", 1, 3)
    period = 3 * 365

# %%
# @st.cache
    def load_data(ticker):
        df = yf.download(ticker, START, TODAY)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df

    stock_data = {}
    data_load_state = st.text("Load data...")
    for stock in stocks:
        data = load_data(stock)
        stock_data[stock] = data

    data_load_state.text("Loading data...done!")

    st.subheader('Raw data for one stock')
    st.write(data.tail())

# %%
    def plot_raw_data(dataPrice):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataPrice['Date'], y=dataPrice['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=dataPrice['Date'], y=dataPrice['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data (TSLA)", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
# %%
    print(stock_data)
    # %%
    plot_raw_data(stock_data['AAPL'])

    train = {}

    # Forecasting
    print('------')
    print(type(train))
    # train_df = pd.DataFrame()
    data_list = []
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

# %%
    train_df = pd.DataFrame(train)
    train_df.to_json(r'./data.json')
    print('succesful write')

# %%
    with open("./data.json", "r") as read_file:
        df2 = json.load(read_file)
    print('successful read')

# %%
    for k in df2.keys():
        df3 = pd.DataFrame(df2[k])
        df3 = df3.set_index('ds')
        st.write(k)
        st.line_chart(df3)

# %%
    print(type(df2))






# %%
if __name__ == '__main__':
    main()

# %%
