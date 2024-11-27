def cv():
    return 60,
def koko():
    mlist=[]
    while 1:
     cv()

xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzQ2OGU2MjI0NWMwMTZjZTJlZjZiMTEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMyNjc3MjE4LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzI3NDQ4MDB9.QzR5K--gq5jWcCpO7fExVqD5r20EGFAtT32pCBtbA5Y'

lastorder=None
lastorder_intent=0
investment_status=0
def buysell(intent,isin,NOS):
    global lastorder,investment_status
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    if lastorder is not None:
        try:
            api_response = api_instance.get_order_status(order_id=lastorder)
            print(api_response)
            if api_response.status=='success':
                investment_status=lastorder_intent
                lastorder=None
        except ApiException as e:
            print("Exception when calling OrderApi->get order status: %s\n" % e.body)
    if lastorder is None and investment_status!=intent:
        if intent>investment_status:
            body=upstox_client.PlaceOrderRequest((intent-investment_status)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
            api_version = '2.0'
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                #if(api_response.status=='success'):
                #    lastorder=ap
                if api_response.status=='success':investment_status=intent
            except ApiException as e:
                exit()
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)
        if intent<investment_status:
            body = upstox_client.PlaceOrderRequest((investment_status-intent)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
            api_version = '2.0'
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                if api_response.status=='success':investment_status=intent
            except ApiException as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)

def buy():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzNjNTZkY2RlMmQ3OTEwMjBlNjZiNTIiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMyMDA3NjQ0LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzIwNTM2MDB9.qDRRrWbox4S4BKqwzvghuoZWgEardIsVd-MmD98Ge00"
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(1, "D", "IOC", 0.0, "string", "NSE_EQ|INE351F01018", "MARKET", "BUY", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
    except ApiException as e:
        print("Exception when calling OrderApi->get order status: %s\n" % e.body)

def sell():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzNjNTZkY2RlMmQ3OTEwMjBlNjZiNTIiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMyMDA3NjQ0LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzIwNTM2MDB9.qDRRrWbox4S4BKqwzvghuoZWgEardIsVd-MmD98Ge00"
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(1, "D", "IOC", 0.0, "string", "NSE_EQ|INE377Y01014", "MARKET", "SELL", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
    except ApiException as e:
        print("Exception when calling OrderApi->get order status: %s\n" % e.body)

def dadw():
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/intraday/NSE_EQ%7CINE00H001014/1minute/'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open('Swiggy.txt','w').write(response.text)


def t():
    import json
    from pprint import pprint
    ms=open('Swiggy.txt','r').read()
    ms=json.loads(ms)['data']['candles']
    ms=list(reversed(ms))
   # pprint(ms[-1][0].split('T')[0])
    dc=[]
    tc=[]
    for n in range(0,len(ms)):
        if n==0:
            tc+=[ms[n]]
        elif ms[n-1][0].split('T')[0]!=ms[n][0].split('T')[0] or n==len(ms)-1:
            dc+=[tc]
            tc=[]
        tc+=[ms[n]]
    return dc
#   pprint(len(dc[-1]))
#    for ntc in dc:       Har roj kitne me start hota
#       print(ntc[0])

                    
def odin():    
    from pprint import pprint
    mc=t()
    acc_bal=100
    per1=0.001
    per2=0.001
    extrm=0
    inv=False
    inv_t=[]
    for n in range(1,len(mc[-1])):
        inv_t+=[inv]
        if inv:
            acc_bal=acc_bal*mc[-1][n][1]/mc[-1][n-1][1]
        if mc[-1][n][1]-mc[-1][n-1][1]> mc[-1][n-1][1]*per1:
            inv=True
            extrm=mc[-1][n][1]
        if mc[-1][n][1]-extrm>0:
            extrm=mc[-1][n][1]
        if mc[-1][n][1]< extrm*(1-per2):
            inv=False
    print(mc[-1][0][0])    
    import matplotlib.pyplot as plt
    plt.plot([1780+ int(s)*20 for s in inv_t])
    plt.plot([s[1] for s in mc[-1] ])
    plt.show()
    
    print(acc_bal)

ntks=0
def ntk():
    global ntks
    ntks+=1
    return [t()[-1][0:ntks]]

isin='NSE_EQ|INE152M01016'
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
    tc=[]
    for n in range(0,len(ms)):
        if n==0:
            tc+=[ms[n]]
        elif ms[n-1][0].split('T')[0]!=ms[n][0].split('T')[0] or n==len(ms)-1:
            dc+=[tc]
            tc=[]
        tc+=[ms[n]]
    return dc
def fenrir():
    import datetime
    print(isin)
    from pprint import pprint
    acc_long_pl=0
    acc_short_pl=0
    lnos=30
    snos=20
    acc_bal1=100
    acc_bal2=100
    r=1          #Margin
  #  sp_12=0.004
  #  sp_34=0.004
    per1=0.003   #sp_12   #0.008     #long buy 
    per2=0.003   #sp_12   #0.008     #long sell
    per3=0.003   #sp_34   #0.008     #short sell
    per4=0.003   #sp_34   #0.008     #short buy
    pl=0
    import time
    while True:
        if 1:time.sleep(10)
        dmc=tk()[-1]             #n hata do#
        extrm_low=dmc[0][1]
        extrm_high=0
        inv=0
        inv_t=[]
        r=1
        if dmc[-1]!=pl:
            pl=dmc[-1]
            print(pl,datetime.datetime.now())
            for n in range(1,len(dmc)):
                pinv=inv
                inv_t+=[inv]
                if inv==1:
                    acc_bal1=acc_bal1*dmc[n][1]/dmc[n-1][1]
                if dmc[n][1]-extrm_low> extrm_low*per1 and inv==0:
                    inv=1
                    extrm_high=dmc[n][1]
                if dmc[n][1]< extrm_high*(1-per2) and inv==1:
                    inv=0

                    
                if dmc[n][1]-extrm_high>0:
                    extrm_high=dmc[n][1]
                if dmc[n][1]-extrm_low<0:
                    extrm_low=dmc[n][1]

                if inv==-1:
                    ssn=ss*dmc[n][1]/dmc[n-1][1]
                    acc_bal2=acc_bal2+ss-ssn
                    ss=ssn
                if dmc[n][1]-extrm_high<- extrm_high*per3 and inv==0:
                    inv=-1
                    extrm_low=dmc[n][1]
                    ss=acc_bal2*r
                if dmc[n][1]> extrm_low*(1+per4) and inv==-1:
                    inv=0
                if n==len(dmc)-1 and inv!=pinv:
                    print('s1')
                if n==len(dmc)-1:
                    print('buysell',inv)
                    pass
                    #buysell(inv,isin,1)
        
def rtd():
    import datetime
    from pprint import pprint
    import datetime
    import upstox_client
    from upstox_client.rest import ApiException

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_version = '2.0'
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))


    acc_long_pl=0
    acc_short_pl=0
    lnos=30
    snos=20
    acc_bal1=100
    acc_bal2=100
    r=1          #Margin
  #  sp_12=0.004
  #  sp_34=0.004
    per1=0.003   #sp_12   #0.008     #long buy 
    per2=0.003   #sp_12   #0.008     #long sell
    per3=0.003   #sp_34   #0.008     #short sell
    per4=0.003   #sp_34   #0.008     #short buy
    pl=0
    dmc=[]
    extrm_low=0 #dmc[0][1]
    extrm_high=0
    inv=0
    inv_t=[]
    r=1
    slp_tm=10 #sleep time
    import time
    while True:
        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            #print(type(api_response))
            #print(datetime.datetime.now())
        except ApiException as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            continue
        dmc+=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
        print(dmc[-1],datetime.datetime.now())
        if len(dmc)==1:
            extrm_high=dmc[0][1]
            extrm_low=dmc[0][1]
            time.sleep(slp_tm)
            continue
    
        n=len(dmc)-1
        inv_t+=[inv]
        if inv==1:
            acc_bal1=acc_bal1*dmc[n][1]/dmc[n-1][1]
        if dmc[n][1]-extrm_low> extrm_low*per1 and inv==0:
            inv=1
            extrm_high=dmc[n][1]
        if dmc[n][1]< extrm_high*(1-per2) and inv==1:
            inv=0

            
        if dmc[n][1]-extrm_high>0:
            extrm_high=dmc[n][1]
        if dmc[n][1]-extrm_low<0:
            extrm_low=dmc[n][1]

        if inv==-1:
            ssn=ss*dmc[n][1]/dmc[n-1][1]
            acc_bal2=acc_bal2+ss-ssn
            ss=ssn
        if dmc[n][1]-extrm_high<- extrm_high*per3 and inv==0:
            inv=-1
            extrm_low=dmc[n][1]
            ss=acc_bal2*r
        if dmc[n][1]> extrm_low*(1+per4) and inv==-1:
            inv=0
        if n==len(dmc)-1:
            print('buysell',inv)
            pass
            #buysell(inv,isin,1)
        if 1:time.sleep(slp_tm)
        


##    print(dmc[0][0])
##    
##    print(per1,per2,per3,per4,acc_bal1,acc_bal2)
##    
##    import matplotlib.pyplot as plt
##    plt.plot([dmc[0][1]+ int(s)*5 for s in inv_t])
##    plt.plot([s[1] for s in dmc ])
##    plt.show()
    
#dadw()
p=rtd()
#buy()
#sell()
