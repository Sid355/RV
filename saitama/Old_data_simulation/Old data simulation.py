import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati

isin='NSE_EQ|INE118H01025'


date='2024-12-19'                           ##########################################


#TODO file naem pre downloaded , not to download again again 
#TODO make the full market quote all these things as functions, so that we can use the program for different apps
#TODO make a permanent data storage of txt files, from which we will do the old data simulation, then we write the data from the last date so only the new dates will be download and added to the previous files  
#TODO make another temporary data storage of the stocks that i want to trade, store data every 10 second
#TODO when we run simulation on old data make a new file combining both permanent old file and new temporary file.
#TODO download all the 1000+ share 6 month old data files all at ones, then every 2 or 3 days download the rest of the files and add it

of=1    ### create new file or simulate an old file 
if of==0: data_file_name=os.path.dirname(os.path.abspath(__file__))+'/Deep Storage/'+Saraswati.name(isin)+'.txt'   ### new file
if of==1: data_file_name=os.path.dirname(os.path.abspath(__file__))+'/Deep Storage/'+'BSE.txt'   # path is creating trouble             #predownloaded file  .txt     old file


def dadw():   ### downloads historical intraday data and save it in a file
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/'+isin.replace('|','%7C')+'/1minute/2024-12-06/2024-03-07'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open(data_file_name,'w').write(response.text)



def t():      ### returns reversed date wise list of all previous intraday data downloaded from dadw() 
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
        if n != 0 and ms[n-1][0].split('T')[0] != ms[n][0].split('T')[0]:
            dc+=[tc]
            tc=[]
        tc+=[ms[n]]
    dc+=[tc]                    # final date ko dc me add kr diye
    return dc                   # Har date ka alag kr rha



def date_list():
    import datetime
   
    from pprint import pprint
    mc=t()
    date_i=0                        
    for s in range(0,len(mc)):
        if mc[s][0][0].find(date)>-1:
            date_i=s
    dmc=mc[date_i]      #  dmc -  make a list of the choosen day
    # print(dmc[0])     #  ['2024-12-06T09:15:00+05:30', 5281.45, 5366.95, 5262, 5365.9, 272932, 0]
    return dmc

#TODO date_range_list 

def date_range_list():
    import datetime
   
    from pprint import pprint
    mc=t()

def maxfinder():              ### input date me kitna profit or loss de rha different percentage execution basis pe
    print(isin)
    dmc=date_list()
    print(dmc[0])
    print(Saraswati.percitest([l[1] for l in dmc]))


def histocast():              ### input date me kitna profit or loss de rha different percentage execution basis pe
    print(isin)
    from pprint import pprint
    mc=t()    #reverse list day wise old data first, new data last
    r=1          #Margin

    for s in range(0,len(mc)):
        if date < mc[0][0][0].split('T')[0]:
            date_i=0
            break
        if date < mc[s][0][0].split('T')[0]:
            date_i=s-1
            break
        if date > mc[-1][0][0].split('T')[0]:
            date_i=len(mc)-1
            break

    print(date_i)
    dmc=mc[date_i] #day choose
    print(dmc[0])         #        ['2024-12-06T09:15:00+05:30', 5281.45, 5366.95, 5262, 5365.9, 272932, 0]
    
    
    input_per=0.3,0.3,0.3,0.3

    pnl=Saraswati.simu([l[1] for l in dmc],*list(input_per))            ### simulation  on open price           P R O B L E M     L[4]     Opening price ko le rha he . abhi dikkat nehni but close price ko lena more realistic hoga...
    # pnl[0]=long profit     pnl[1]=short profit
    # Note: agar closing price pe dekhna he to both pnl me and values= s[1] me 4 lena hoga
    # but 4 lene me hamesha loss dikhara rha as compare to 1 ..... Why
    print(pnl[0],pnl[1])
    inv_t=pnl[2]          # investment status 0,1,-1  list  
    values = [s[1] for s in dmc]   
    # Calculate percentage change relative to the first value
    start_value = values[0]
    percentage_change = [(v - start_value) / start_value * 100 for v in values]
    
    
    # Plot the graph
    import matplotlib.pyplot as plt
    for i in range(0,len(percentage_change)-1):
        plt.plot([i,i+1],[percentage_change[i],percentage_change[i+1]],color="red" if inv_t[i]==-1 else "green" if inv_t[i]==1 else "blue")
    plt.text(0, 1.02, f'{dmc[0][0].split('T')[0]}    {input_per}' , transform=plt.gca().transAxes, fontsize=12, color='blue')
    plt.text(0.56, 1.02, f'   {round(pnl[0],2)} ' , transform=plt.gca().transAxes, fontsize=12, color='green')
    plt.text(0.71, 1.02, f'   {round(pnl[1],2)} ' , transform=plt.gca().transAxes, fontsize=12, color='red')
    color_pnl=round(pnl[0]+pnl[1]-200,2)
    col = 'blue' if color_pnl >= 0 else 'red'
    plt.text(0.9, 1.02, color_pnl , transform=plt.gca().transAxes, fontsize=12, color=col)
    
    bar_heights = [v[5] for v in dmc]
    max_height=1  #min(percentage_change)+1
    scaled_bar_heights= [h* max_height / max(bar_heights) for h in bar_heights]
    for i in range(0,len(percentage_change)-1):
        start = i
        end = i+1
        b= min(percentage_change)-min(percentage_change)%0.5-0.5
        plt.bar(start +0.5, scaled_bar_heights[i], width=1, bottom=b, align='center', alpha=0.4, edgecolor='black', label="Bars" if i == 0 else "")
    plt.grid(True)
    plt.show()

    print(len(dmc),len(inv_t))
    


PTR=   2     # programm to run    0=nothing

if PTR==1: dadw()
if PTR==2: histocast()
if PTR==3: maxfinder()