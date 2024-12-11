xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzU4ZmY0NTliOTYzNzAwMDFmNDUzYjIiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzMzODg1NzY1LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzM5NTQ0MDB9.sHA-ZY-o_gT174iyMlvHJPw49JfGZneE9zvXJnjdiPA'

isin='NSE_EQ|INE0ONG01011'

NOS=1


slp_tm=30     #sleep time                                                          ###############################################################################
    

lastorder=None
lastorder_intent=0
investment_status=0


def simu(data,p1,p2,p3,p4):
    strategist=shadow_stalker(data[0])
    strategist.lb_per=p1
    strategist.ls_per=p2
    strategist.ss_per=p3
    strategist.sb_per=p4
    inv=0
    inv_t=[]
    r=1
    acc_bal1=100
    acc_bal2=100
    for n in range(1,len(data)):
        inv_t+=[inv]
        if inv==1:
            acc_bal1=acc_bal1*data[n]/data[n-1]
        if inv==-1:
            ssn=ss*data[n]/data[n-1]
            acc_bal2=acc_bal2+ss-ssn
            ss=ssn
        old_inv=inv
        inv=strategist.advise(inv,data[n])     # advise mang rha he ki abhika investment status ye he and new price ye he to kya krna chahiye
        if old_inv!=-1 and inv==-1:              # advise mangne ke badd ka investment
            ss=acc_bal2*r
    return acc_bal1,acc_bal2,inv_t
    
    

def percitest(data):
    percentages=[0.01,0.02,0.03,0.04,0.05]
    n=len(percentages)
    max=0,argmax=[float('inf')]*4
    for p1 in range(0,n):
        for p2 in range(0,n):
            for p3 in range(0,n):
                for p4 in range(0,n):
                    prapti=simu(data,p1,p2,p3,p4)
                    if prapti[0]+prapti[1]>max:
                        max=prapti[0]+prapti[1]
                        argmax=[p1,p2,p3,p4]
    return argmax



class shadow_stalker:
    lb_per= 0.1        #long buy 
    ls_per= 0.1        #long sell
    ss_per= 0.1        #short sell
    sb_per= 0.1        #short buy
    extrm_low=0       #dmc[0][1]
    extrm_high=0
    def __init__(self,initial_price):
        self.extrm_high=initial_price
        self.extrm_low=initial_price
    def advise(self,inv,new_price):  
        
        if new_price< self.extrm_high*(1-self.ls_per/100) and inv== 1:
            inv=0
            self.extrm_low=new_price

        if new_price> self.extrm_low*(1+self.sb_per/100) and inv== -1:
            inv=0
            self.extrm_high=new_price
            
        if new_price-self.extrm_low> self.extrm_low*self.lb_per/100 and inv==0:
            inv=1
            self.extrm_high=new_price
            
        if new_price-self.extrm_high<- self.extrm_high*self.ss_per/100 and inv==0:
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

def buy(order_type='I'):
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

def sell(order_type='I'):
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
 
    dmc=[]
    inv=0            # Investment Intention
    inv_t=[]         # Historical Investment Intention List
    
    strategist=None


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
            strategist=shadow_stalker(inv,dmc[0][1])
            time.sleep(slp_tm)
            continue
    
        n=len(dmc)-1
        inv_t+=[inv]

        inv=strategist.advise(inv,dmc[n][1])

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
    #alpha_hunt()
    #buy('D')
    #sell('D')
    #print(orderstatus(241210025065761))
    pass