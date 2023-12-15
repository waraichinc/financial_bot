import pandas as pd 

def load_data():
    return pd.read_csv("../data/EndOfDayData_2023-05-30.csv")

def get_market_data(query_terms):
    df = load_data()
    pass
