import Broker
broker=Broker.upstox



isin_map = {
    1: ("ITI",         "NSE_EQ|INE248A01017"),
    2: ("MOBIKWIK",    "NSE_EQ|INE0HLU01028"),
    3: ("TATAMOTORS",  "NSE_EQ|INE155A01022"),
    4: ("SWIGGY",      "NSE_EQ|INE00H001014"),
    5: ("OLAELEC",     "NSE_EQ|INE0LXG01040"),
    6: ("ADANIGREEN",  "NSE_EQ|INE364U01010"),
    7: ("ADANIPOWER",  "NSE_EQ|INE814H01011"),
    8: ("PAYTM",       "NSE_EQ|INE982J01020"),
    9: ("HAL",         "NSE_EQ|INE066F01020"),
    10:("HINDALCO",    "NSE_EQ|INE038A01020"),
    11:("ITC",         "NSE_EQ|INE154A01025"),
    12:("KALYANKJIL",  "NSE_EQ|INE303R01014"),
    13:("TATAPOWER",   "NSE_EQ|INE245A01021"),
    14:("TATASTEEL",   "NSE_EQ|INE081A01020"),
    15:("SWIGGY",      "NSE_EQ|INE00H001014"),
    16:("SUZLON",      "NSE_EQ|INE040H01021"),
    17:("RELIANCE",    "NSE_EQ|INE002A01018"),
    18:("RELIGARE",    "NSE_EQ|INE621H01010"),
    19:("RAYMOND",     "NSE_EQ|INE301A01014"),
    20:("PREMIERENE",  "NSE_EQ|INE0BS701011"),
    21:("ONGC",        "NSE_EQ|INE213A01029"),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
#    16:("",  "NSE_EQ| "),
}


isin_codes = [value[1] for value in isin_map.values()]
symbol_codes= [value[0] for value in isin_map.values()]
print(isin_codes)
print(symbol_codes)

def get_only_one_isin(isin_quest):      #isin_quest = 8   
    return isin_map.get(isin_quest, (None, None))
symbol, isin = get_only_one_isin(3)                              ##################################################################
print(f"ISIN Quest  => symbol: {symbol}, isin: {isin}")


def get_multiple_isin(*user_input):     # user_input = 2,5,7
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

available_money=350



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

        inv=advisor.advise(inv,data[n],[p1,p2,p3,p4])     # advise mang rha he ki abhika investment status ye he and new price ye he to kya krna chahiye
        

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
    percentages=[0.1,0.15,0.2]    #,0.25,0.3
    tm=[]
    for p4 in percentages:
        for p2 in percentages:
            for p3 in percentages:
                for p1 in percentages:
                    tm+=[[p1,p2,p3,p4]]
    return tm
    

def percitest(data):
    weight=0
    max_pnl=-float('inf')
    argmax=[float('inf')]*4
    tem_list=[]
    v=combination_pers()
    #long_pnl=-float('inf')
    #short_pnl=-float('inf')
    for vi in v:
        p1,p2,p3,p4=vi[0],vi[1],vi[2],vi[3]

        prapti=simu(data,p1,p2,p3,p4)       ###################### simulation

        avg=0*(p1+p2+p3+p4)/4
        pnl = prapti[0]+prapti[1] - weight* max( abs(p1-avg) ,abs(p2-avg) ,abs(p3-avg) ,abs(p4-avg) )            
        if pnl==max_pnl:    # if equal
            tem_list+=[[p1,p2,p3,p4]]
        if pnl > max_pnl:
            max_pnl=pnl
            argmax=[p1,p2,p3,p4]
            long_pnl=prapti[0]
            short_pnl=prapti[1]
            #total_pnl=prapti[0]+prapti[1]
            tem_list=[argmax]     #remake list  
           
    print(tem_list)                   
    return long_pnl,short_pnl,max_pnl,argmax



class shadow_stalker:
    extrm_low=0       #dmc[0][1]
    extrm_high=0
    ############ add a variable status=l/s that shows whether long or short position is taken. make run for the first 3 min with read time 1 sec and take benifits
    def __init__(self,initial_price):
        self.extrm_high = initial_price
        self.extrm_low = initial_price
    
    def advise(self,inv_status,new_price,per_arg):  
        self.lb_per= per_arg[0]        #long buy 
        self.ls_per= per_arg[1]        #long sell
        self.ss_per= per_arg[2]        #short sell
        self.sb_per= per_arg[3]        #short buy
        
        intent = inv_status

        if new_price < self.extrm_high*(1-self.ls_per/100) and inv_status == 1:
            intent = 0
            self.extrm_low = new_price

        if new_price > self.extrm_low*(1+self.sb_per/100) and inv_status == -1:
            intent = 0
            self.extrm_high=new_price
            
        if new_price > self.extrm_low + self.extrm_low*self.lb_per/100 and inv_status == 0:
            intent = 1
            self.extrm_high = new_price
            
        if new_price < self.extrm_high - self.extrm_high*self.ss_per/100 and inv_status == 0:
            intent = -1
            self.extrm_low = new_price

        if new_price > self.extrm_high:
            self.extrm_high = new_price

        if new_price < self.extrm_low:
            self.extrm_low = new_price

        return intent

def time_difference(obs_time='09:14:30'):                ############################## time difference 9:14 tak
    import time
    from datetime import datetime   
    current_time=time.time()
    same_date = datetime.fromtimestamp(current_time)
    h,m,s = map(int,obs_time.split(':'))
    obs_datetime = same_date.replace(hour=h,minute=m,second=s,microsecond=0)
    return obs_datetime.timestamp()-current_time

def alpha_hunt(isin=isin,per_arg=[0.2,0.3,0.2,0.3]):           ## The main buy sell file
    import time 
    td=time_difference('9:14:30')
    if td>0:
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)

    slp_tm = 30     #sleep time                                ###############################################################################
    

    dmc=[]
    inv_status=0            
    inv_t=[]         # Historical investment status list
    
    strategist=None


    from datetime import datetime
    while True:
        api_response= broker.ful_mar_quo(isin)
        if api_response == None:
            time.sleep(slp_tm)
            continue

        dmc+=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
        print(dmc[-1],datetime.now())

        if len(dmc) == 1:
            strategist=shadow_stalker(dmc[0][1])     # __init__ ko de rehe ho
            time.sleep(slp_tm)
            continue
    
        n=len(dmc)-1   # can we put -1 in place of n for the latest price
        inv_t+=[inv_status]

        intent = strategist.advise(inv_status,dmc[n][1],per_arg)

        print(f'intent= {intent}, inv_status= {inv_status}')

        if inv_status == intent: 
            time.sleep(slp_tm)
            continue
        
        print(datetime.now())

        if broker.buysell(inv_status,intent,isin,NOS):
            inv_status = intent             ### if intended order executed successfully then make the intent our new inv_status
        


        #execution price difference
        if 0:
            api_response = broker.ful_mar_quo(isin)
            if api_response == None:
                time.sleep(slp_tm)
                continue
            new_api_res=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
            print('Time of execution',new_api_res)                                                            ##############            I added
        
        if 1:time.sleep(slp_tm)
        

### add inv_status=0 in beta_slasher input. so that we can immediately purchase after evaluation in mother india
def beta_slasher(isin,inv_status,quantity,per_arg,pur_price):           ## modified alpha_hunt
    global isin_codes,symbol_codes
    import time 
    from datetime import datetime
    symbol=symbol_codes[isin_codes.index(isin)]
    exiting=False
    slp_tm = 10     #sleep time                                                          ###############################################################################
    
    dmc=[]
    inv_list=[]         # Historical investment status list
    strategist=None     # do we really need this
    start_time=time.time()
    print(f'first purchased price: {pur_price}')
    first_pur_price= pur_price

    while True:
        api_response= broker.ful_mar_quo(isin)    # ful_mar_quo me dedo...agar api_response None aya 2 times try krne ke baad...to wo output exit dega....so hum yahan position se exit ho jayenge.
        if api_response == None:
            time.sleep(slp_tm)
            continue

        dmc+=[[api_response.data[next(iter(api_response.data))].timestamp,api_response.data[next(iter(api_response.data))].last_price]]
        print(dmc[-1],datetime.now())

        if len(dmc) == 1:
            strategist=shadow_stalker(dmc[0][1])     # __init__ ko de rehe ho
            time.sleep(slp_tm)
            continue
    
        inv_list+=[inv_status]

        intent = strategist.advise(inv_status,dmc[-1][1],per_arg)      ############# A D V I C E  ################

        print(f'{symbol}, intent= {intent}, inv_status= {inv_status}')
        #exp_bal = bal + inv_status *NOS* dmc[-1][1]
        exp_pnl = (-pur_price + dmc[-1][1]) * inv_status 
        pnl_per = (exp_pnl / first_pur_price) * 100

        
        if time.time()-start_time > 180  and pnl_per < 0.2:
            # i can directly square off all positions
            intent=0
            exiting=True
            if inv_status == 0:
                mother_india()
        if time.time()-start_time > 180 and pnl_per >= 0.2:
            slp_tm=3
        if time.time()-start_time > 1 and pnl_per >= 0.5:
            intent=0
            exiting=True
            if inv_status == 0:
                mother_india()             
        if time.time()-start_time > 60 and pnl_per < 0:              # square off all positions   
            isin_codes.remove(isin)
            symbol_codes.remove(symbol)  
            intent=0
            exiting=True
            if inv_status == 0:
                mother_india()

        if inv_status == intent: 
            time.sleep(slp_tm)
            continue
        
        print(datetime.now())
        
        purchase_status,new_pur_price = broker.buysell(inv_status,intent,isin,quantity)

        if purchase_status == True:    # True if purchase status is complete
            #pur_price+=(inv_status-intent)*NOS*pur_price
            pur_price += (inv_status-intent) * new_pur_price
            inv_status = intent    ### if intended order executed successfully then make the intent our new inv_status
            
        ##problem- long or short pos to 0 hua tabhi purchase_status true hoga n hum exir kr skte. agar 0 me hi tha to purchase_status
        ##complete nehni hoga n we will not be able to stop.

        if exiting == True:    ## you can take this inside exit condition....checks
            mother_india()

        time.sleep(slp_tm)
        
hk=None

def mother_india():
    global isin_codes,symbol_codes
    import time 

    obs_time=10              #################
    
    max_pnl = float('-inf')
    max_argmax = []
    max_isin = None
    print(isin_codes)
    global hk
    hk=pulse_fetcher()
    hk.data[isin]


    for isin in isin_codes:
        print(f'checking {isin}')
        symbol = symbol_codes[isin_codes.index(isin)] 
        print(f'checking symbol {symbol}')
        data= broker.intraday_candle_data(isin)
        print(data)
        if data == None:
            print(f"No data retrieved for ISIN: {isin}. Removing {symbol} and skipping to next.")
            isin_codes.remove(isin)
            symbol_codes.remove(symbol)
            continue

        data=data.data.candles
        data=list(reversed(data))
        obs_data=data[-obs_time:]
        print(f'Checking data and percitest for {isin}-{symbol}')
        print(f"Obervational data:{obs_data}")
        
        _,_,pnl,argmax=percitest([l[4] for l in obs_data])
        #argmax is a list or what
        if pnl > max_pnl:
            max_pnl,max_argmax,max_isin,int_ltp = pnl, argmax, isin, obs_data[-2][4]   # 2nd last intraday last traded price
        #time.sleep(0.1)
    
    #b=bread()
    #b.calu=False
    max_symbol = symbol_codes[isin_codes.index(max_isin)]
    print(f"Maximum Profit: {max_pnl} from isin={max_isin}, symbol={max_symbol} argmax={max_argmax}")
    
    api_response = broker.ful_mar_quo(max_isin)
    print(api_response)
    if api_response == None:
        symbol_codes.remove(max_symbol)
        isin_codes.remove(max_isin)
        print(f"after remove isin {max_isin} the rest isin's are {isin_codes}")
        mother_india()

        

    if int_ltp <= api_response.data[next(iter(api_response.data))].last_price: 
        quantity = broker.quant_purchasable(available_money,max_isin,'BUY')
        print(f'buying initially.')
        os = broker.buy(quantity,max_isin,order_type='I')
    if int_ltp >  api_response.data[next(iter(api_response.data))].last_price: 
        quantity = broker.quant_purchasable(available_money,max_isin,'SELL')
        print(f'selling initially.')
        os = broker.sell(quantity,max_isin,order_type='I')
    print(f'os: {os}')
    if os[0] == False:
        print(f'removing isin {max_isin} and symbol {max_symbol}')
        symbol_codes.remove(max_symbol)
        isin_codes.remove(max_isin)
        print(isin_codes)
        mother_india()
    if os[0] == True:   # find a way to immediately invest
        inv_status=os[1]
        pur_price=os[2]
        beta_slasher(max_isin,inv_status,quantity,max_argmax,pur_price)
    

class pulse_fetcher():
    calu=True
    t=None
    data={}
    length=0
    lock=None
    global isin_codes

    def __init__(self):
        import threading
        self.t=threading.Thread(target=self.data_ticker)
        self.t.start()
        self.lock=threading.Lock()
        for isin in isin_codes:
            self.data[isin]=[] 
        
    def data_ticker(self):
        import time
        while self.calu:
            asd=','.join(isin_codes)
            all_data = broker.full_market_quote_multiple_instrument(asd)
            if 0:self.lock.acquire()
            for isin in isin_codes:
                symbol = symbol_codes[isin_codes.index(isin)]
                self.data[isin]+=[all_data.data['NSE_EQ:'+symbol].last_price]
            if 0:self.lock.release()
            self.length+=1
            time.sleep(1)


    
if __name__ == '__main__':
        
    PTR= 7

    if PTR==0: pass
    if PTR==1: alpha_hunt(isin,[0.2,0.1,0.3,0.1])
    if PTR==2: broker.buy('I')
    if PTR==3: broker.sell('I')
    if PTR==4: print(broker.orderstatus(241210025065761))
    if PTR==5: pass #percitest(data,weight=0)
    if PTR==6: mother_india()
    if PTR==7: pulse_fetcher.data_ticker()
    


