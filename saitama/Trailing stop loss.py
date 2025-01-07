

xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzY4YmJlMDVlZTcxNDMxZTZiMzZiNTciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM0OTE3MDg4LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzQ5OTEyMDB9.9LPwRX2UplBcCo59jasHO3NC3Bp_PSamRNrPPdarJ4I'

isin='NSE_EQ|INE0HLU01028'

NOS=1

buy_percentage = 1/100 *  0.1
sell_percentage= 1/100 *  0.1


order_type="D"            ### Intraday order="I"                Delivery order="D"

sleep_time=60
def orderstatus(order):
    import upstox_client
    from upstox_client.rest import ApiException

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    try:
        api_response = api_instance.get_order_status(order_id=order)
        return api_response
    except ApiException as e:
        print("Exception when calling OrderApi->get order status: %s\n" % e.body)

def ful_mar_quo():            ### return full market quote
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

def time_difference():                ############################## time difference 9:14 tak
    import time
    from datetime import datetime
    p=time.time()
    n=datetime.fromtimestamp(p)
    n=n.replace(hour=9,minute=14,second=0,microsecond=0)
    return n.timestamp()-p

def buy(order_type):
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, order_type, "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)

def sell(order_type):
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, order_type, "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)


def trailing_stoploss_buy():     ### Not DONE
    import time
    td=time_difference()
    if td>0:                                             # to sleep until the market opens
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)
    lower_extremum=0
    while True:
        f=ful_mar_quo()
        ltp=f.data[next(iter(f.data))].last_price
        if ltp < lower_extremum:
            lower_extremum=ltp
            print('new extremum='+str(lower_extremum))
        if ltp>lower_extremum*(1+buy_percentage):
            buy(order_type)
            print('buy order price='+str(ltp),'extremum='+str(lower_extremum))
            break
        time.sleep(sleep_time)



def trailing_stoploss_sell():
    import time
    td=time_difference()
    if td>0:                                           # to sleep until the market opens
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)
    upper_extremum=0
    while True:
        f=ful_mar_quo()
        ltp=f.data[next(iter(f.data))].last_price
        if ltp > upper_extremum:
            upper_extremum=ltp
            print('new extremum='+str(upper_extremum))
        if ltp<upper_extremum*(1-sell_percentage):
            sell(order_type)
            print('sell order price='+str(ltp),'extremum='+str(upper_extremum))
            break
        time.sleep(sleep_time)








execution='ts'     ###   'b'- buy   and   's'- sale

if execution=='b': buy('D')   # Not done
if execution=='s': sell('D')
if execution=='tb': trailing_stoploss_buy()   # Not done
if execution=='ts': trailing_stoploss_sell()



