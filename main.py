import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd

IEX_API_Key = ''
tickers = [
            'MSFT',
            'AAPL',
            'AMZN',
            'GOOG',
            'FB',
            'BRK.B',
            'JNJ',
            'WMT',
            'V',
            'PG'
            ]
tickers = ",".join(tickers)
endpoints = 'price,stats'
token = ""
HTTP_request = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={tickers}&types={endpoints}&range=1y&token={token}'
# HTTP_request = f"https://sandbox.iexapis.com/stable/stock/IBM/quote?token={token}"

raw_data = pd.read_json(HTTP_request)
output_data = pd.DataFrame(pd.np.empty((0,4)))
print(HTTP_request)

for ticker in raw_data.columns:

  company_name = raw_data[ticker]['stats']['companyName']
  stock_price = raw_data[ticker]['price']
  dividend_yield = raw_data[ticker]['stats']['dividendYield']
    
  new_column = pd.Series([ticker, company_name, stock_price, dividend_yield])
  output_data = output_data.append(new_column, ignore_index = True)
  print(output_data)
