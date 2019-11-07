from datetime import datetime
import pandas as pd
import numpy as np

class EffietientFrontier:
    def __init__(self, symbol_list, start_date='', end_date=''):
        self.symbol_list = symbol_list
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.date_range = pd.date_range(self.start_date, self.end_date)

    def get_data(self,ohlc_coll):
        final = pd.DataFrame({'Date': self.date_range})
        date_range_filter = {"$gte": self.start_date, "$lt": self.end_date}

        for symbol in self.symbol_list:
            df_symbol = pd.DataFrame(
                list(ohlc_coll.find({'Symbol': symbol, 'Date': date_range_filter}, {'Close': 1, 'Date': 1, '_id': 0})))

            df_symbol = df_symbol.rename(columns={'Close': symbol})
            if not df_symbol.empty:
                # print('successful for {} - Max date = {} - Min Date = {}'.format(symbol,df_symbol.Date.max(),df_symbol.Date.min()))
                final = pd.merge(final, df_symbol, how='outer', on='Date')
            else:
                pass
                # print('successful for {}'.format(symbol))
        return final

    @staticmethod
    def get_change_prec_cov_and_returns(df):
        # calculate daily and annual returns of the stocks
        returns_daily = df.pct_change()
        returns_annual = returns_daily.mean() * 250

        # get daily and covariance of returns of the stock
        cov_daily = returns_daily.cov()
        cov_annual = cov_daily * 250

        return cov_annual,returns_annual

    @staticmethod
    def get_mean_variance_portfolio(cov_annual,returns_annual,comapny_list,num_portfolios=50000):
        # empty lists to store returns, volatility and weights of imiginary portfolios
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []

        # set the number of assets
        num_assets = len(comapny_list)

        # set random seed for reproduction's sake
        np.random.seed(101)

        # populate the empty lists with each portfolios returns,risk and weights
        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, returns_annual)
            volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
            sharpe = returns / volatility
            sharpe_ratio.append(sharpe)
            port_returns.append(returns)
            port_volatility.append(volatility)
            stock_weights.append(weights)

        # a dictionary for Returns and Risk values of each portfolio
        portfolio = {'Returns': port_returns,
                     'Volatility': port_volatility,
                     'Sharpe Ratio': sharpe_ratio}

        # extend original dictionary to accomodate each ticker and weight in the portfolio
        for counter, symbol in enumerate(comapny_list):
            portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]

        # make a nice dataframe of the extended dictionary
        df = pd.DataFrame(portfolio)

        # get better labels for desired arrangement of columns
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in comapny_list]

        # reorder dataframe columns
        df = df[column_order]

        return df

    @staticmethod
    def get_min_vola_max_shapre(df):

        # find min Volatility & max sharpe values in the dataframe (df)
        min_volatility = df['Volatility'].min()
        max_sharpe = df['Sharpe Ratio'].max()

        # use the min, max values to locate and create the two special portfolios
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
        min_variance_port = df.loc[df['Volatility'] == min_volatility]

        return (min_variance_port.T,sharpe_portfolio.T)