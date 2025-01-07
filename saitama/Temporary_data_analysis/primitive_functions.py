
isin='NSE_EQ|INE982J01020'

def dadw():   ### downloads historical intraday data and save it in a file                     ##Not required anymore
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/intraday/'+isin.replace('|','%7C')+'/1minute'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    open("E:/RV/extra/payt.txt",'w').write(response.text)

dadw()