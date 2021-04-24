import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    style.use('seaborn-darkgrid')
    sns.set_context('notebook')
    sns.set_palette('gist_heat')

    START = "2018-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title("Stock Prediction App")

    stocks = ("AAPL", "GOOG", "MSFT", "TSLA")
    selected_stock = st.selectbox("Select dataset for prediction", stocks)

    # n_years = st.slider("Years of prediction:", 1, 3)
    period = 3 * 365


    @st.cache
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


    def plot_raw_data(dataPrice):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataPrice['Date'], y=dataPrice['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=dataPrice['Date'], y=dataPrice['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)


    plot_raw_data(data)

    train = {}
    # Forecasting
    for k in stock_data.keys():
        df = stock_data[k]
        df = df[['Date', 'Close']]
        df = df.rename(columns={'Date': 'ds', 'Close': 'y'})
        train[k] = df
    # print(type(tmp))
    # print(tmp)
    print('\n------------------')
    print('\n----formatted fisrt value')
    print(df)
    print('\n------------------')
    print('\n----unformatted value')
    # print(data)
    print('\n------------------')
    print('\n------------------')
    # train_df = pd.DataFrame(data = tmp, columns=stocks)
    print(train.keys())

    text_file = open("dump_file.txt", "w")
    for k in train.keys():
        st.line_chart(train[k].loc[:,'y'])
        text_file.write(str({k : train[k].values}))
    text_file.close()



        # plot_raw_data(train[k])
    #     plt.figure(figsize=(17, 5))
    #     st.write(f'Forecast plot for {3} years')
    #     fig1 = plot_plotly(m, forecast)
        # st.plotly_chart(fig1)
    #
    #     sns.lineplot(data=train[k], x='date', y='item_cnt_month')
    #     sns.lineplot(data=train[k], x='date', y='year_mean', color='forestgreen')
    #     plt.legend(['item_cnt_month', 'year_average'])

    # m = Prophet()
    # m.fit(df_train)
    # future = m.make_future_dataframe(periods=period)
    # forecast = m.predict(future)
    #
    # forecast_copy = forecast.copy()
    # forecast_copy['ds'] = pd.to_datetime(forecast_copy['ds']).dt.date
    #
    # # Show and plot forecast
    # st.subheader('Forecast data')
    # st.write(forecast_copy.tail())
    #
    # st.write(f'Forecast plot for {n_years} years')
    # fig1 = plot_plotly(m, forecast)
    # st.plotly_chart(fig1)
    #
    # st.write("Forecast components")
    # fig2 = m.plot_components(forecast)
    # st.write(fig2)


if __name__ == '__main__':
    main()
