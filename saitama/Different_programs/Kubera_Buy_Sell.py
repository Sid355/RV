isin='INE155A01022'
txt_file='Tata.txt'




def dadw():
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/NSE_EQ%7C'+isin+'/1minute/2024-12-06/2023-11-12'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open(txt_file,'w').write(response.text)


                    
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


def fenrir():              ### input date me kitna profit or loss de rha different percentage execution basis pe
    import datetime
    print(isin)
    from pprint import pprint
    mc=t()
    acc_long_pl=0
    acc_short_pl=0
    lnos=30
    snos=20
    acc_bal1=100
    acc_bal2=100
    r=1          #Margin
    per1=0.0005  #When to buy 
    per2=0.0005  #long sell
    per3=0.0005  #short sell
    per4=0.0005   #short buy
    date='2024-12-05'                           ##########################################
    date_i=0
    for s in range(0,len(mc)):
        if mc[s][0][0].find(date)>-1:
            date_i=s
    dmc=mc[date_i] #day choose
    extrm_high=dmc[0][1]
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
        if dmc[n][1]> extrm_low*(1+per4) and inv==-1:
            inv=0
        
        

    print(dmc[0][0])
    
    print(acc_bal1,acc_bal2)
    
    import matplotlib.pyplot as plt
 
#   plt.plot([s[1] for s in dmc ])
    values = [s[1] for s in dmc]
    # Calculate percentage change relative to the first value
    start_value = values[0]
    percentage_change = [(v - start_value) / start_value * 100 for v in values]
    # Plot the graph
    for i in range(0,len(percentage_change)-300):
        plt.plot([i,i+1],[percentage_change[i],percentage_change[i+1]],color="red" if inv_t[i]==-1 else "green" if inv_t[i]==1 else "blue")

    #plt.plot(percentage_change)
    #plt.plot([percentage_change[0] + s*max(percentage_change) for s in inv_t],color="green")
    print(len(dmc),len(inv_t))
    plt.show()




#dadw()
#fenrir()
