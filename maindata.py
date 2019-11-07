import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import numpy as np
from EffitientFrontierApp import *

# create mongo Client
client = MongoClient("localhost", 27017)

# connect to db
db_capitalmarket = client["capitalmarket"]

# Connect to collection
company_master = db_capitalmarket.coll_company_master
ohlc = db_capitalmarket.coll_ohlc


#company_list = list(company_master.find({}, {'Symbol': 1, '_id': 0}))
#company_list = [list(i.values()) for i in company_list]
#company_list = [item for sublist in company_list for item in sublist]


start = '2008-01-01'
end = '2019-01-01'

company_list = ['BALRAMCHIN', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'MAHABANK']

def get_effitient_frontier(start,end,company_list):
    frontier = EffietientFrontier(company_list, start, end)

    df_data = frontier.get_data(ohlc)
    df_data.set_index('Date', inplace=True)

    #call static methods
    cov_annual,returns_annual = frontier.get_change_prec_cov_and_returns(df=df_data)

    num_portfolios=50000
    df_mean_variance_portfolio = frontier.get_mean_variance_portfolio(cov_annual,returns_annual,company_list,num_portfolios)

    min_variance_portfolio , max_sharpe_portfolio ,max_returns_portfolio = \
        frontier.get_effitient_portfolio(df_mean_variance_portfolio)

    min_variance_portfolio.columns = ['min_variance_portfolio']
    max_sharpe_portfolio.columns = ['max_sharpe_portfolio']
    max_returns_portfolio.columns = ['max_returns_portfolio']

    df = min_variance_portfolio.join(max_sharpe_portfolio).join(max_returns_portfolio)

    


    
    return (df)

    # print(min_variance_portfolio)
    # print(max_sharpe_portfolio)
    # print(max_returns_portfolio)


#print(get_effitient_frontier(start,end,company_list))