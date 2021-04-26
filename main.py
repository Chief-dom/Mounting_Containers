from datamover import DataMover
from datetime import date
# %%
def main():
    today = date.today().strftime("%Y-%m-%d")
    mover = DataMover("2018-01-01", today)
    ticker_list = ["AAPL", "GOOG", "MSFT", "TSLA"]
    df = mover.load_datas(ticker_list)
    mover.write_json(df)




# %%
if __name__ == '__main__':
    main()    
        