xs2kn='eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI4TEFKRzkiLCJqdGkiOiI2NzdiMjc3OTk2MGY1NDEwOTY3MDMwZDciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM2MTI0MjgxLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzYyMDA4MDB9.S1t9k9LS0JKTG3OgL5ytJzUepFJsU8G-wMadZC-zatM'

#Make a class of upstox and take all function buy,sell,full market quote inside. make a variable broker=upstox/kotak. whenever you call a function write broker.buy()

def get_only_one_isin(isin_quest):      #isin_quest = 8
    isin_map = {
        1: ("ITI",         "NSE_EQ|INE248A01017"),
        2: ("MOBIKWIK",    "NSE_EQ|INE0HLU01028"),
        3: ("TATAMOTORS",  "NSE_EQ|INE155A01022"),
        4: ("SWIGGY",      "NSE_EQ|INE00H001014"),
        5: ("OLAELEC",     "NSE_EQ|INE0LXG01040"),
        6: ("ADANIGREEN",  "NSE_EQ|INE364U01010"),
        7: ("ADANIPOWER",  "NSE_EQ|INE814H01011"),
        8: ("PAYTM",       "NSE_EQ|INE982J01020"),
    }
    return isin_map.get(isin_quest, (None, None))

symbol, isin = get_only_one_isin(5)
print(f"ISIN Quest  => symbol: {symbol}, isin: {isin}")


def get_multiple_isin(*user_input):     # user_input = 2,5,7
    isin_map = {
        1: ("ITI",         "NSE_EQ|INE248A01017"),
        2: ("MOBIKWIK",    "NSE_EQ|INE0HLU01028"),
        3: ("TATAMOTORS",  "NSE_EQ|INE155A01022"),
        4: ("SWIGGY",      "NSE_EQ|INE00H001014"),
        5: ("OLAELEC",     "NSE_EQ|INE0LXG01040"),
        6: ("ADANIGREEN",  "NSE_EQ|INE364U01010"),
        7: ("ADANIPOWER",  "NSE_EQ|INE814H01011"),
        8: ("PAYTM",       "NSE_EQ|INE982J01020"),
    }
        
    result = []
    for number in user_input:
        symbol, isin = isin_map.get(number, (None, None))
        if symbol and isin:
            # Append the tuple in the order (ISIN, symbol)
            result.append((isin, symbol))
        else:
            # If there's no match, we'll just skip or print a message
            print(f"No data found for number: {number}")

    return result
    # output_list = get_multiple_isin(2, 5, 7)
    # print("\nFinal list of (ISIN, symbol) tuples:")
    # print(output_list)







NOS=1    # No of shares to trade


slp_tm=60     #sleep time                                                          ###############################################################################
    

lastorder=None
lastorder_intent=0
investment_status=0

#TODO 

def simu(data,p1,p2,p3,p4):
    advisor=shadow_stalker(data[0])
    advisor.lb_per=p1
    advisor.ls_per=p2
    advisor.ss_per=p3
    advisor.sb_per=p4
    inv=0
    inv_t=[]
    r=1
    long_bal=100
    short_bal=100
    long_charges=0
    short_charges=0
    intraday_charges=(1/100)*0.04   ### 0.03512 exact combining buy and sell side
    #margin_charge=0
    for n in range(1,len(data)):
        inv_t+=[inv]
        if inv==1:
            long_bal=long_bal*data[n]/data[n-1]
        if inv==-1:
            ssn=ss*data[n]/data[n-1]
            short_bal=short_bal+ss-ssn
            ss=ssn                                                                                         ####    may be MISTAKE   PROBLEM if ss=100 initially and share price drops 10 then bal=110 then ss should be 110
        old_inv=inv

        inv=advisor.advise(inv,data[n])     # advise mang rha he ki abhika investment status ye he and new price ye he to kya krna chahiye
        

        if old_inv!=-1 and inv==-1:              # advise mangne ke badd ka investment
            ss=short_bal*r
        if old_inv!=inv:
            if inv==1:
                long_charges+=intraday_charges*long_bal
                #print(long_charges)     ### problem - pehle charge katke uska kitna profit loss hua wo dekhte hne
            if inv==-1:
                short_charges+=intraday_charges*short_bal
                    ### problem
    
    long_bal=long_bal-long_charges
    short_bal=short_bal-short_charges
    
    return long_bal,short_bal,inv_t

def combination_pers():    # gives all combination of the given percentages
    percentages=[0.1,0.15,0.2,0.25,0.3]
    tm=[]
    for p4 in percentages:
        for p2 in percentages:
            for p3 in percentages:
                for p1 in percentages:
                    tm+=[[p1,p2,p3,p4]]
    return tm
    

def percitest(data,weight=0):
    pro_dev=-float('inf')
    argmax=[float('inf')]*4
    tem_list=[]
    v=combination_pers()
    #long_pnl=-float('inf')
    #short_pnl=-float('inf')
    for vi in v:
        p1,p2,p3,p4=vi[0],vi[1],vi[2],vi[3]
        prapti=simu(data,p1,p2,p3,p4)       # simulation

        avg=0*(p1+p2+p3+p4)/4
        pnl_dev = prapti[0]+prapti[1] - weight* max( abs(p1-avg) ,abs(p2-avg) ,abs(p3-avg) ,abs(p4-avg) )            
        if pnl_dev==pro_dev:    # if equal
            tem_list+=[[p1,p2,p3,p4]]
        if pnl_dev > pro_dev:
            pro_dev=pnl_dev
            argmax=[p1,p2,p3,p4]
            long_pnl=prapti[0]
            short_pnl=prapti[1]
            tem_list=[argmax]     #remake list         
    print(tem_list)                   
    return long_pnl,short_pnl,argmax



class shadow_stalker:
    lb_per= 0.15        #long buy 
    ls_per= 0.1       #long sell
    ss_per= 0.1        #short sell
    sb_per= 0.3        #short buy
    extrm_low=0       #dmc[0][1]
    extrm_high=0
    ############################################ add a variable status=l/s that shows whether long or short position is taken. make run for the first 3 min with read time 1 sec and take benifits
    def __init__(self,initial_price):
        self.extrm_high = initial_price
        self.extrm_low = initial_price
    
    def advise(self,inv,new_price):  
        
        if new_price < self.extrm_high*(1-self.ls_per/100) and inv == 1:
            inv = 0
            self.extrm_low = new_price

        if new_price > self.extrm_low*(1+self.sb_per/100) and inv == -1:
            inv = 0
            self.extrm_high=new_price
            
        if new_price > self.extrm_low + self.extrm_low*self.lb_per/100 and inv == 0:
            inv = 1
            self.extrm_high = new_price
            
        if new_price < self.extrm_high - self.extrm_high*self.ss_per/100 and inv == 0:
            inv = -1
            self.extrm_low = new_price

        if new_price > self.extrm_high:
            self.extrm_high = new_price

        if new_price < self.extrm_low:
            self.extrm_low = new_price

        return inv

def time_difference():                ############################## time difference 9:14 tak
    import time
    from datetime import datetime
    p=time.time()
    n=datetime.fromtimestamp(p)
    n=n.replace(hour=9,minute=14,second=0,microsecond=0)
    return n.timestamp()-p


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
            strategist=shadow_stalker(dmc[0][1])
            time.sleep(slp_tm)
            continue
    
        n=len(dmc)-1   # can we put -1 in place of n for the latest price
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
        
    PTR= 0

    if PTR==0: pass
    if PTR==1: alpha_hunt()
    if PTR==2: buy('I')
    if PTR==3: sell('I')
    if PTR==4: print(orderstatus(241210025065761))
    if PTR==5: percitest()
    



 #historical_data()
    #data_save()
    #print(name(isin))
    #dadw()
    #alpha_hunt()
    #buy('D')
    #sell('D')
    #print(orderstatus(241210025065761))