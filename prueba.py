import config
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from alpha_vantage.fundamentaldata import FundamentalData

## Variables globales

cases_to_names = {
    'q_BS': 'quarterly_balance_sheet',
    'q_IS': 'quarterly_income_statement',
    'q_CF': 'quarterly_cash_flow',
    'a_BS': 'annual_balance_sheet',
    'a_IS': 'annual_income_statement',
    'a_CF': 'annual_cash_flow'
}
data_dir = ''
tickers = ['META', 'CEPU', 'IBM']

def fundamental_api_call(case: str, ticker: str, fd):
    '''
    Due to the API limit of 5 calls per minute, this function was desinged so
    that every 5th download can impose a sleep time of a minute.
    Parameters
    ----------
    case : str
        The download switch statement.
    ticker : str
        The ticker to download the data for
    fd : Fundamental Data Downloader
        The fundamental data downloader for AlphaVantage.
    Returns
    ----------
    None
    '''

    if case == 'a_IS':
        data = fd.get_income_statement_annual(ticker)
    elif case == 'a_BS':
        data = fd.get_balance_sheet_annual(ticker)
    elif case == 'a_CF':
        data = fd.get_cash_flow_annual(ticker)
    elif case == 'q_IS':
        data = fd.get_income_statement_quarterly(ticker)
    elif case == 'q_BS':
        data = fd.get_balance_sheet_quarterly(ticker)
    elif case == 'q_CF':
        data = fd.get_cash_flow_quarterly(ticker)
    
    data[0].to_csv(data_dir + ticker + '_' + cases_to_names[case] + '.csv', 
                   index = False)
    
    return

def get_fundamentals(tickers: list):
    '''
    Using the AlphaVantage API, obtain the historical fundamental data for a
    set of tickers
    Parameters
    ----------
    tickers : list
        The list of tickers to download the fundamentals for
    Returns
    -------
    None
    
    Notes
    -----
    On a free API key, only 500 calls per day are allowed. Given that this
    function downloads 6 different statements, a maximum of 83 tickers can be
    considered. Likewise, only 5 API calls can be made per minute, so a sleep
    step is included at every 5 downloads.
    '''

    fd = FundamentalData(config.api_key, output_format = 'pandas')

    # This counter allows us to halt after 5 api calls in a single minute
    numero_descarga = 0
    
    # List to store and print the incomplete downloads
    lista_descargas_incompletas = []

    for ticker in tqdm(tickers):
      for case in cases_to_names.keys():
        try:
          fundamental_api_call(case, ticker, fd)
        except Exception as e:
          lista_descargas_incompletas.append(ticker)
          print(ticker, ':', e)
            
        # Check the API limit per minute has not been breached
        numero_descarga += 1
        if numero_descarga%5 == 0:
          time.sleep(65)
    
    print('descargas incompletas:', list(set(lista_descargas_incompletas)))

    return

if __name__ == '__main__':
  get_fundamentals(tickers)