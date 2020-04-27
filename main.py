import os, ssl
import boto3
# if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
# getattr(ssl, '_create_unverified_context', None)):
#   ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import xlsxwriter

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

output_data.columns = ['Ticker', 'Company Name', 'Stock Price', 'Dividend Yield']
output_data.set_index('Ticker', inplace=True)
output_data['Dividend Yield'].fillna(0,inplace=True)

writer = pd.ExcelWriter('stock_market_data.xlsx', engine='xlsxwriter')
output_data.to_excel(writer, sheet_name='Stock Market Data')

header_template = writer.book.add_format(
        {
            'font_color': '#ffffff',
            'bg_color': '#135485',
            'border': 1
        }
    )

string_template = writer.book.add_format(
        {
            'bg_color': '#DADADA',
            'border': 1
        }
    )

dollar_template = writer.book.add_format(
        {
            'num_format':'$0.00',
            'bg_color': '#DADADA',
            'border': 1
        }
    )

percent_template = writer.book.add_format(
        {
            'num_format':'0.0%',
            'bg_color': '#DADADA',
            'border': 1
        }
    )

writer.sheets['Stock Market Data'].conditional_format('A1:D1', 
                             {
                                'type':     'cell',
                                'criteria': '<>',
                                'value':    '"None"',
                                'format':   header_template
                                }
                            )

writer.sheets['Stock Market Data'].conditional_format('A2:B11', 
                             {
                                'type':     'cell',
                                'criteria': '<>',
                                'value':    '"None"',
                                'format':   string_template
                                }
                            )

writer.sheets['Stock Market Data'].conditional_format('C2:C11', 
                             {
                                'type':     'cell',
                                'criteria': '<>',
                                'value':    '"None"',
                                'format':   dollar_template
                                }
                            )

writer.sheets['Stock Market Data'].conditional_format('D2:D11', 
                             {
                                'type':     'cell',
                                'criteria': '<>',
                                'value':    '"None"',
                                'format':   percent_template
                                }
                            )

writer.sheets['Stock Market Data'].set_column('B:B', 32)
writer.sheets['Stock Market Data'].set_column('C:C', 18)
writer.sheets['Stock Market Data'].set_column('D:D', 20)

writer.save()

s3 = boto3.resource('s3')
s3.meta.client.upload_file('stock_market_data.xlsx', 'stock-tracker-test', 'stock_market_data.xlsx', ExtraArgs={'ACL':'public-read'})
