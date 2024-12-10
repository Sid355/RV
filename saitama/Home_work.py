import Saraswati
xs2kn=Saraswati.xs2kn
isin='NSE_EQ|INE0LXG01040'            ##Saraswati.isin
NOS=1                                 ##Saraswati.NOS


def bssb(n):    # Define the repeating pattern
    pattern = [1, 2, 2, 1]         ## B S S B B S S B 
    return pattern[(n) % len(pattern)]


def home_work():
    import time
    td=Saraswati.time_difference()
    if td>0:
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)

    from pprint import pprint
    import datetime
    import time,json,jsonpickle
    import upstox_client
    from upstox_client.rest import ApiException

    configuration = upstox_client.Configuration()
    configuration.access_token = xs2kn
    api_version = '2.0'
    api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

    import random
    
    #print(ran_num)
    #start_time=datetime.datetime.now().strftime("%H:%M")
    import os.path
    if os.path.isfile('check'):
        l=jsonpickle.decode(open('check','r').read())
    else: l=[]
    noet=10  ##no of execution time
    file=open('check','a+')
    for n in range(0,noet):
        ran_num = random.randint(1, 180)    ## (1,300) 5 sec I left for execution delay. i omited this idea
        time.sleep(ran_num)
        print('ran='+str(ran_num)+str(ful_mar_quo()))
        p=ful_mar_quo()
        if bssb(n)==1:
            d='b'
            t=buy()
        else:
            d='s'
            t=sell()
        l+=[[p,d,t]]
        open('check','w').write(jsonpickle.dumps(l))
        time.sleep(5*60-ran_num)    
    
    

#print(buy())
#Saraswati.orderstatus('241204025003953')   

#sell()
#print(home_work())
#print(ful_mar_quo())

#home_work()


