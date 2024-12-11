import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati

isin='NSE_EQ|INE118H01025'

data_file_name=os.path.dirname(os.path.abspath(__file__))+'/'+Saraswati.name(isin)+'.txt'


def dadw():   ### downloads historical intraday data and save it in a file
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/'+isin.replace('|','%7C')+'/1minute/2024-12-06/2024-03-07'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open(data_file_name,'w').write(response.text)



def t():      ### returns date wise list of all previous intraday data downloaded from dadw() 
    import json
    from pprint import pprint
    #{"status":"success","data":{"candles":[  ["2024-12-06T15:29:00+05:30",817.55,818,817,818,75421,0],["2024-12-06T15:28:00+05:30",817.95,818,817,817.85,100533,0],["2024-12-06T15:27:00+05:30",818.3,818.35,817.5,817.95,65663,0] }
    ms=open(data_file_name,'r').read()
    ms=json.loads(ms)['data']['candles']
    ms=list(reversed(ms))                                  # reversed to old data first
   # pprint(ms[-1][0].split('T')[0])
    dc=[]   # date wise list         [  [all data of 2024-03-17]   [all data of 2024-03-18]  ]
    tc=[]   # temporary list
    for n in range(0,len(ms)):
        if n!=0 and ms[n-1][0].split('T')[0]!=ms[n][0].split('T')[0]:
            dc+=[tc]
            tc=[]
        tc+=[ms[n]]
    dc+=[tc]                    # final date ko dc me add kr diye
    return dc                   # Har date ka alag kr rha
#   pprint(len(dc[-1]))
#    for ntc in dc:       Har roj kitne me start hota
#       print(ntc[0])





def histocast():              ### input date me kitna profit or loss de rha different percentage execution basis pe
    import datetime
    print(isin)
    from pprint import pprint
    mc=t()
    r=1          #Margin

    date='2024-12-06'                           ##########################################

    date_i=0
    for s in range(0,len(mc)):
        if mc[s][0][0].find(date)>-1:
            date_i=s
    dmc=mc[date_i] #day choose
    
    import matplotlib.pyplot as plt
 
    p=Saraswati.simu([l[1] for l in dmc],0.2,0.2,0.2,0.2)
    print(p[0],p[1])
    inv_t=p[2]
    values = [s[1] for s in dmc]
    # Calculate percentage change relative to the first value
    start_value = values[0]
    percentage_change = [(v - start_value) / start_value * 100 for v in values]
    # Plot the graph
    for i in range(0,len(percentage_change)-1):
        plt.plot([i,i+1],[percentage_change[i],percentage_change[i+1]],color="red" if inv_t[i]==-1 else "green" if inv_t[i]==1 else "blue")

    print(len(dmc),len(inv_t))
    plt.show()


if 0:dadw()
if 1:histocast()