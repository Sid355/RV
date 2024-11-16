def cv():
    return 60,
def koko():
    mlist=[]
    while 1:
     cv()

def dadw():
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/NSE_EQ%7CINE118H01025/1minute/2024-11-13/2023-11-12'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open('BSE.txt','w').write(response.text)


def t():
    import json
    from pprint import pprint
    ms=open('BSE.txt','r').read()
    ms=json.loads(ms)['data']['candles']
    ms=list(reversed(ms))
   # pprint(ms[-1][0].split('T')[0])
    dc=[]
    tc=[]
    for n in range(0,len(ms)):
        if n==0:
            tc+=[ms[n]]
        elif ms[n-1][0].split('T')[0]!=ms[n][0].split('T')[0]:
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





def fenrir():    
    from pprint import pprint
    mc=t()
    acc_long_pl=0
    acc_short_pl=0
    lnos=30
    snos=20
    acc_bal1=100
    acc_bal2=100
    r=1          #Margin
    per1=0.002   #When to buy 
    per2=0.004   #long sell
    per3=0.005   #short sell
    extrm_high=0
    date='2024-10-11'
    date_i=0
    for s in range(0,len(mc)):
        if mc[s][0][0].find(date)>-1:
            date_i=s
    dmc=mc[date_i] #day choose
    extrm_low=dmc[0][1]
    inv=0
    inv_t=[]
    r=1
    for n in range(1,len(dmc)):
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
        if dmc[n][1]> extrm_low*(1+per2) and inv==-1:
            inv=0
        
        

    print(dmc[0][0])
    
    print(acc_bal1,acc_bal2)
    
    import matplotlib.pyplot as plt
    plt.plot([dmc[0][1]+ int(s)*20 for s in inv_t])
    plt.plot([s[1] for s in dmc ])
    plt.show()
    
#dadw()
fenrir()
