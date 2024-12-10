import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati
isin='NSE_EQ|INE248A01017' 

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

