




def data_save():
    import datetime
    from pprint import pprint
    import datetime
    import upstox_client
    from upstox_client.rest import ApiException
    import time

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_version = '2.0'
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
    dmc=[]
    for k in  range(0,6*(60*6+15)):      ##Har 10 sec ka data download krna he
        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            #print(type(api_response))
            #print(datetime.datetime.now())
            dmc+=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
            print(dmc[-1])
        except Exception as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            continue
        time.sleep(10)
    s=''
    for l in dmc:
        s+=l[0]+' '+str(l[1])+'\n'
    s=s[0:-1]
    open(isin+'data.txt').write(s)



    
def historical_data():          ############## Historical data download krke add krte jata he ek file me
    import requests
    import json
    new_isin=isin.split('|')[0]+'%7C'+isin.split('|')[1]

    date='2024-09-06/2024-09-06'        ################################################################################
    
    url = 'https://api.upstox.com/v2/historical-candle/'+new_isin+'/1minute/'+date
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    filename=name(isin)+'.txt'
    import os.path
    if os.path.isfile(filename):
        res_json=response.json()
        l1=res_json['data']['candles']
        ms=open(filename,'r').read()
        l0=json.loads(ms)['data']['candles']
        mila=None
        for k in range(0,len(l1)):
            if l0[0][0]==l1[k][0]:
                mila=k
                break
        if mila!=None:
            res_json['data']['candles']=l1[0:mila]+l0
            open(filename,'w').write(json.dumps(res_json))
        else:
            res_json['data']['candles']=l1+l0
            open(filename,'w').write(json.dumps(res_json))
    else:
        open(filename,'w').write(response.text)

