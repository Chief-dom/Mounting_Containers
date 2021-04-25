# %%
def main():
    import datamover
    mover = DataMover()
    ticker_list = ["AAPL", "GOOG", "MSFT", "TSLA"]
    df = load_datas(ticker_list)
    write_json(df)




# %%
if __name__ == '__main__':
    main()    
        