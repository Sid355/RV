xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzUxMGQ4NzNkNmRjODFjYWNhMDkzMTkiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMzMzY1MTI3LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzM0MzYwMDB9.TigEwLwD0UoL9Z2uvfCm-mjF4KhVx5BDo0lfNjsbDk8'

isin='NSE_EQ|INE377Y01014'

NOS=1

per_decrease=0.001

order_type="D"            ### Intraday order="I"                Delivery order="D"

def name(isin):               ### It will give the name
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
    try:
        api_response = api_instance.get_full_market_quote(isin, api_version)
        #print(type(api_response))
        #print(datetime.datetime.now())
        return api_response.data[next(iter(api_response.data))].symbol
    except Exception as e:
        print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

def ful_mar_quo():
    import datetime
    import time
    from pprint import pprint
    import upstox_client
    from upstox_client.rest import ApiException

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_version = '2.0'
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
    while True:
        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            if api_response.status=='success':
                return api_response
            #print(type(api_response))
            #print(datetime.datetime.now())
        except Exception as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
        time.sleep(10)
                

def buy():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "D", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
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
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "D", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
    except ApiException as e:
        print("Exception when calling OrderApi->get order status: %s\n" % e.body)


def time_difference():                ############################## time difference
    import time
    from datetime import datetime
    p=time.time()
    n=datetime.fromtimestamp(p)
    n=n.replace(hour=9,minute=14,second=0,microsecond=0)
    return n.timestamp()-p

def trailing_stoploss():
    import time
    td=time_difference()
    if td>0:
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)
    extremum=0
    while True:
        f=ful_mar_quo()
        ltp=f.data[next(iter(f.data))].last_price
        if ltp > extremum:
            extremum=ltp
            print('new extremum='+str(extremum))
        time.sleep(10)
        if ltp<extremum*(1-per_decrease):
            sell()
            print('sell order price='+str(ltp),'extremum='+str(extremum))
            break
        


#trailing_stoploss()


#buy()
#sell()