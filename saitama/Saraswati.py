xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzU3YTJkOTI3MmIxNTJjYzJlOTJkNzYiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMzNzk2NTY5LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzM4NjgwMDB9.pA9VBTDGaiUQHv6uNmuAegR1-kwf1AiBMFGq63GHQ1c'

isin='NSE_EQ|INE040A01034'

NOS=1


slp_tm=30     #sleep time                                                          ###############################################################################
    

lastorder=None
lastorder_intent=0
investment_status=0

class shadow_stalker:
    lb_per=0.001        #long buy 
    ls_per=0.001        #long sell
    ss_per=0.001        #short sell
    sb_per=0.001        #short buy
    extrm_low=0       #dmc[0][1]
    extrm_high=0
    def __init__(self,initial_price):
        self.extrm_high=initial_price
        self.extrm_low=initial_price
    def advise(self,inv,new_price):  
        
        if new_price< self.extrm_high*(1-self.ls_per) and inv== 1:
            inv=0
            self.extrm_low=new_price

        if new_price> self.extrm_low*(1+self.sb_per) and inv== -1:
            inv=0
            self.extrm_high=new_price
            
        if new_price-self.extrm_low> self.extrm_low*self.lb_per and inv==0:
            inv=1
            self.extrm_high=new_price
            
        if new_price-self.extrm_high<- self.extrm_high*self.ss_per and inv==0:
            inv=-1
            self.extrm_low=new_price

        if new_price-self.extrm_high>0:
            self.extrm_high=new_price
        if new_price-self.extrm_low<0:
            self.extrm_low=new_price
        return inv

def name(isin):               ### It will give the name of any given isin
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

def time_difference():                ############################## time difference 9:14 tak
    import time
    from datetime import datetime
    p=time.time()
    n=datetime.fromtimestamp(p)
    n=n.replace(hour=9,minute=14,second=0,microsecond=0)
    return n.timestamp()-p

def buy():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "BUY", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)

def sell():
    import upstox_client
    from upstox_client.rest import ApiException
    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
    body = upstox_client.PlaceOrderRequest(NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
    api_version = '2.0'
    try:
        api_response = api_instance.place_order(body, api_version)
        print(api_response)
        if api_response.status=='success':
            os=orderstatus(api_response.data.order_id)
            return (os,os.data.status)
            
    except Exception as e:
        print("Exception %s\n" % e.body)

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
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)
        if intent<investment_status:
            body = upstox_client.PlaceOrderRequest((investment_status-intent)*NOS, "I", "IOC", 0.0, "string", isin, "MARKET", "SELL", 0, 0.0, False)
            api_version = '2.0'
            try:
                api_response = api_instance.place_order(body, api_version)
                print(api_response)
                if api_response.status=='success':investment_status=intent
            except Exception as e:
                print("Exception when calling OrderApi->get order status: %s\n" % e.body)



def alpha_hunt():           ## The main buy sell file
    import time
    td=time_difference()
    if td>0:
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)

    import datetime
    from pprint import pprint
    import upstox_client
    from upstox_client.rest import ApiException

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_version = '2.0'
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))


    r=1                      # Margin
 
    per1=0.0015        #long buy 
    per2=0.0015        #long sell
    per3=0.0015        #short sell
    per4=0.0015        #short buy
    extrm_low=0       #dmc[0][1]
    extrm_high=0
    dmc=[]
    inv=0            # Investment Intention
    inv_t=[]         # Historical Investment Intention List
    

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

        if dmc[n][1]< extrm_high*(1-per2) and inv== 1:
            inv=0
            extrm_low=dmc[n][1]

        if dmc[n][1]> extrm_low*(1+per4) and inv== -1:
            inv=0
            extrm_high=dmc[n][1]
            
        if dmc[n][1]-extrm_low> extrm_low*per1 and inv==0:
            inv=1
            extrm_high=dmc[n][1]
            
        if dmc[n][1]-extrm_high<- extrm_high*per3 and inv==0:
            inv=-1
            extrm_low=dmc[n][1]

        if dmc[n][1]-extrm_high>0:
            extrm_high=dmc[n][1]
        if dmc[n][1]-extrm_low<0:
            extrm_low=dmc[n][1]



        print('buysell',inv)
        pass
        buysell(inv,isin,NOS)                            ##buysell program
        try:
            api_response = api_instance.get_full_market_quote(isin, api_version)
            #print(type(api_response))
            #print(datetime.datetime.now())
        except ApiException as e:
            print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)
            continue
        new_api_res=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
        print('Time of execution',new_api_res)                                                            ##############            I added
        if 1:time.sleep(slp_tm)
        

if __name__ == '__main__':
    #historical_data()
    #data_save()
    #print(name(isin))
    #dadw()
    alpha_hunt()
    #buy()
    #sell()
    pass
