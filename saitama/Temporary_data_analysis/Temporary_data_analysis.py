import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati

xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2Nzc3NjNmZDI1ZTE0Nzc0MjY5MzNhODMiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM1ODc3NjI5LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzU5NDE2MDB9.1024l5KHSjhg5LaI1st1zVsp4QzpcXTSAK1ux48bp2w'

isin_quest=  1 

if isin_quest== 1 : symbol,isin= 'ITI'          ,'NSE_EQ|INE248A01017'
if isin_quest== 2 : symbol,isin= 'MOBIKWIK'     ,'NSE_EQ|INE0HLU01028'
if isin_quest== 2 : symbol,isin= 'TATAMOTORS'   ,'NSE_EQ|INE155A01022'
if isin_quest== 2 : symbol,isin= 'SWIGGY'       ,'NSE_EQ|INE00H001014'
if isin_quest== 2 : symbol,isin= 'OLAELEC'      ,'NSE_EQ|INE0LXG01040'
if isin_quest== 2 : symbol,isin= 'ADANIGREEN'   ,'NSE_EQ|INE364U01010'
if isin_quest== 2 : symbol,isin= 'ADANIPOWER'   ,'NSE_EQ|INE814H01011'
if isin_quest== 2 : symbol,isin= 'PAYTM'        ,'NSE_EQ|INE982J01020'

def tk():
    import requests
    import json
    url = 'https://api.upstox.com/v2/historical-candle/intraday/'+isin.replace('|','%7C')+'/1minute/'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    ms=json.loads(response.text)['data']['candles']
    ms=list(reversed(ms))
   # pprint(ms[-1][0].split('T')[0])
    dc=[]
    tc=[ms[0][0]]
    for n in range(1,len(ms)):
        if ms[n-1][0].split('T')[0]!=ms[n][0].split('T')[0]:
            dc+=[tc]
            tc=[]
        tc+=[ms[n]]
    dc+=[tc]
    return dc



def maxfinder():              ### input date me kitna profit or loss de rha different percentage execution basis pe
    import json
    with open('E:/RV/saitama/Temporary_data_analysis/temp_txt_files/payt.txt','r') as file:
        data = json.load(file)

    t_list=[element[4] for element in data['data']['candles']]  # only closed data list
    t_list=t_list[-10:]
    print(Saraswati.percitest([s for s in t_list],weight=0))



def full_market_quotes():
    import requests

    url = 'https://api.upstox.com/v2/market-quote/'+isin.replace('|','%7C')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {xs2kn}'
    }

    response = requests.get(url, headers=headers)

    print(response.text)


if __name__ == '__main__':
        
    PTR= 2

    if PTR==0: pass
    if PTR==1: maxfinder()
    if PTR==2: full_market_quotes()
   