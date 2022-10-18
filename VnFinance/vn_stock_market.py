import requests
from bs4 import BeautifulSoup
import pandas as pd
import certifi
import datetime as dt
from datetime import timezone
import sqlite3

certifi.where()

#Convert string: 2001-01-03T00:00:00.000Z into datetime object
#import datetime as dt


def convert_time_tcbs(d):
    d = pd.to_datetime(d)
    d = pd.to_datetime(d).dt.tz_localize(None)
    return d


#TCBS does not provide benchmark's data: VNINDEX, VN30, v.v...
#Panel data just apply with Daily, Weekly, Monthly and abbrivate as D, W, M respectively.
def get_stock_data(symbol, freq):
    symbol = symbol.upper()
    freq = freq.upper()
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/bars-long-term?ticker={symbol}&type=stock&resolution={freq}&from=0&to=1672419600'
    r = requests.get(url).json()
    df = pd.DataFrame(r['data'])
    
    # Check whether data is empty or not
    if df.empty:
        print(f"There is no stock: {symbol}")
        print("Please enter again!")
    else:
        ticker = r['ticker']
        df['tradingDate'] = convert_time_tcbs(df['tradingDate'])
        
        #Set name for column
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Date']
        df.set_index('Date', inplace=True)
        df['Ticker'] = symbol
        
        return df


#Get Large Shareholders from TCBS's API
def get_large_shareholders(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{symbol}/large-share-holders'
    r = requests.get(url).json()
    try:
        r['message'] == 'Bad Request'
    except:
        df = pd.DataFrame(r['listShareHolder'])
        #Set standard owning percentage
        df['ownPercent'] = df['ownPercent']*100
    
        return df
    else:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")


#Get Key Officers from TCBS's API
def get_key_officers(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{symbol}/key-officers?page=0&size=20'
    r = requests.get(url).json()
    
    try:
        r['message'] == 'Bad Request'
    except:
        df = pd.DataFrame(r['listKeyOfficer'])
        #Set standard owning percentage
        df['ownPercent'] = df['ownPercent']*100
    
        return df
    else:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")


#Get Sub Companies from TCBS's API
def get_sub_company(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{symbol}/sub-companies?page=0&size=30'
    r = requests.get(url).json()
    
    try:
        r['message'] == 'Bad Request'
    except:
        df = pd.DataFrame(r['listSubCompany'])
        
        #Set standard owning percentage
        df['ownPercent'] = df['ownPercent']*100
        
        return df
    else:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")


#Get Divident payment histories from TCBS's API
def get_div_history(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{symbol}/dividend-payment-histories?page=0&size=40'
    r = requests.get(url).json()
    
    try:
        r['message'] == 'Bad Request'
    except:
        df = pd.DataFrame(r['listDividendPaymentHis'])
        #Drop unnecessary column
        df = df.drop('no', axis=1)
        
        #Set standard time
        df['exerciseDate'] = pd.to_datetime(df['exerciseDate'])
        
        #Set standard cash dividend percentage
        df['cashDividendPercentage'] = df['cashDividendPercentage']*100
        
        return df
    else:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")


#Get Insider dealing from TCBS's API
def get_ins_dealing(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/company/{symbol}/insider-dealing?page=0&size=100'
    r = requests.get(url).json()
    
    try:
        r['message'] == 'Bad Request'
    except:
        df = pd.DataFrame(r['listInsiderDealing'])
        #Drop unnecessary column
        df = df.drop('no', axis=1)
        
        #Set standard time
        df['anDate'] = pd.to_datetime(df['anDate'])
        
        #Set index
        df = df.set_index('anDate')
        return df
    else:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")


#Get Volume Trading of Foreign Investors from TCBS's API
def get_vol_foreign(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/data-charts/vol-foreign?ticker={symbol}'
    r = requests.get(url).json()
    df = pd.DataFrame(r['listVolumeForeignInfoDto'])
    
    if df.empty:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")
    else:
        #Convert to standard time
        df['dateReport'] = pd.to_datetime(df['dateReport'])
        
        #Set index for panel data
        df.set_index('dateReport', inplace=True)
        
        return df


#Get Activities news of each company from TCBS's API
def get_activity_news_com(symbol):
    #Get data from TCBS's API and convert it to panel data
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{symbol}/activity-news?page=0&size=60'
    r = requests.get(url).json()
    df = pd.DataFrame(r['listActivityNews'])
    if df.empty:
        print(f"There is no symbol: {symbol}")
        print("Please enter again!")
    else:
    #Convert to standard time
        df['publishDate'] = pd.to_datetime((df['publishDate']))
        
        #Convert to standard percentage change
        df['priceChangeRatio'] = df['priceChangeRatio']*100
        df['priceChangeRatio1W'] = df['priceChangeRatio1W']*100
        df['priceChangeRatio1M'] = df['priceChangeRatio1M']*100
        
        #Drop unnecessary columns
        df.drop('id', axis=1, inplace=True)
        
        return df

#Get Activities news of each industry from TCBS's API
def get_activity_news_ind(ind_code):
    #Get data from TCBS's API and convert it to panel data
    ind_code = ind_code.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/news/activities?fData={ind_code}&fType=industryId&page=0&size=60'
    r = requests.get(url).json()
    
    if "listActivityNews" in r.keys():
        df = pd.DataFrame(r['listActivityNews'])
        if df.empty:
            print(f"There is no industry code: {ind_code}")
            print("Please enter again!")
        else:
            #Convert to standard time
            df['publishDate'] = pd.to_datetime((df['publishDate']))
            
                # Convert to standard percentage change
            df['priceChangeRatio'] = df['priceChangeRatio']*100
            df['priceChangeRatio1W'] = df['priceChangeRatio1W']*100
            df['priceChangeRatio1M'] = df['priceChangeRatio1M']*100
            
            #Drop unnecessary columns
            df.drop('id', axis=1, inplace=True)
        
            return df
    else:
        print(f"There is no industry code: {ind_code}")
        print("Please enter again!")


#Get Income Statement Data from TCBS's API
def get_is_data(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/finance/{symbol}/incomestatement?yearly=0&isAll=true'
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    
    # statements
    if df.empty:
        print(f"There is no stock: {symbol}")
        print("Please enter again!")
    else:
        return df


#Get Balance Sheet Data from TCBS's API
def get_bs_data(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/finance/{symbol}/balancesheet?yearly=0&isAll=true'
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    
    # statements
    if df.empty:
        print(f"There is no stock: {symbol}")
        print("Please enter again!")
    else:
        return df


#Get Cash Flow Statement Data from TCBS'S API
def get_cf_data(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/finance/{symbol}/cashflow?yearly=0&isAll=true'
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    
    # statements
    if df.empty:
        print(f"There is no stock: {symbol}")
        print("Please enter again!")
    else:
        return df


#Get Financial Ratio from TCBS'S API
def get_fs_ratio(symbol):
    symbol = symbol.upper()
    url = f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/finance/{symbol}/financialratio?yearly=0&isAll=true'
    r = requests.get(url).json()
    df = pd.DataFrame(r)
    
    # statements
    if df.empty:
        print(f"There is no stock: {symbol}")
        print("Please enter again!")
    else:
        return df


#Get columns headers of Financial Statement from TCBS's API
def get_headers(data):
    header_names = list(data.columns.values)
    return header_names


if __name__ == "__main__":
    print("Hello World")