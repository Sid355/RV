import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati

symbol,isin = 'PAYTM'        ,'NSE_EQ|INE982J01020'

# 'ITI'          ,'NSE_EQ|INE248A01017'
# 'MOBIKWIK'     ,'NSE_EQ|INE0HLU01028'
# 'TATAMOTORS'   ,'NSE_EQ|INE155A01022'
# 'SWIGGY'       ,'NSE_EQ|INE00H001014'
# 'OLAELEC'      ,'NSE_EQ|INE0LXG01040'
# 'ADANIGREEN'   ,'NSE_EQ|INE364U01010'
# 'ADANIPOWER'   ,'NSE_EQ|INE814H01011'
# 'PAYTM'        ,'NSE_EQ|INE982J01020'
  
date='2024-12-02'                           ##########################################

def program_selection():
        
    PTR=   3     # programm to run    0=nothing

    if PTR==0: pass
    elif PTR==1: retrieve()                  #('WOL3D','NSE_EQ|INE0OO201011') #('AKG','NSE_EQ|INE00Y801016')
    elif PTR==2: histocast()
    elif PTR==3: maxfinder()
    elif PTR==4: dynamic_horizon()


#TODO evaluator
#TODO if suddenly take a -1 position from 1 does the charge get deduced only once or twice i
#TODO file naem pre downloaded , not to download again again 
#TODO make the full market quote all these things as functions, so that we can use the program for different apps
#TODO make a permanent data storage of txt files, from which we will do the old data simulation, then we write the data from the last date so only the new dates will be download and added to the previous files  
#TODO make another temporary data storage of the stocks that i want to trade, store data every 10 second
#TODO when we run simulation on old data make a new file combining both permanent old file and new temporary file.
#TODO download all the 1000+ share 6 month old data files all at ones, then every 2 or 3 days download the rest of the files and add it

#TODO if file already exist then dont download only add teh latest data.   first find the last date of previous file then input that date in donwload dadw() date/ current date

def symbol_find():            ### For a given ISIN ('NSE_EQ|INE0HLU01028') of this form find symbol
    import pandas as pd
    symbol=None
    target_isin=isin.split('|')[1]

    if symbol==None:    
        EQ_logs = pd.read_csv("E:/RV/saitama/Deep_storage/EQUITY_L.csv")
        # Strip leading and trailing whitespace from column names
        EQ_logs.columns = EQ_logs.columns.str.strip()
        #match_EQ = EQ_logs[EQ_logs['ISIN NUMBER'] == target_isin]
        #if bool(match_EQ):       symbol=EQ_logs['SYMBOL'][n]
        for n in range(0,len(EQ_logs['ISIN NUMBER'])):  
            if EQ_logs['ISIN NUMBER'][n] == target_isin:
                symbol=EQ_logs['SYMBOL'][n]
            break

    if symbol is None:
        SME_logs = pd.read_csv("E:/RV/saitama/Deep_storage/SME_EQUITY_L.csv")
        SME_logs.columns = SME_logs.columns.str.strip()
        for n in range(0,len(SME_logs['ISIN_NUMBER'])):  
            if SME_logs['ISIN_NUMBER'][n] == target_isin:
                symbol=SME_logs['SYMBOL'][n]
            break

    if symbol is None:
        print(f"Symbol for this ISIN is not present in both the .csv file.")  


def retrieve(symbol=symbol,isin=isin):         ### Retrieve data. if not available creates in additional folder. Modify it to combine the data. also modiy the deep_storage to download and modify a single data file     
    import json
    file_name= f'{symbol}_{isin.split('|')[1]}.txt'
    file_paths = [  f"E:/RV/saitama/Deep_storage/Equity_storage/{file_name}",
                    f"E:/RV/saitama/Deep_storage/SME_storage/{file_name}",
                    f"E:/RV/saitama/Deep_storage/Additional_storage/{file_name}"         ]
    
    data=None 
    for file_path in file_paths:
        if os.path.isfile(file_path):
            try:
                with open(file_path,'r') as file:
                    data = json.load(file)
                return data
            except json.JSONDecodeError:
                print(f"[Error] Decoding JSON from {file_path}. Possibly corrupt or invalid JSON.")
            except Exception as e:
                print(f"[Error] An error occurred while reading {file_path}: {e}")

    if data is None:        
        import requests    
        from datetime import date
        today = date.today()
        start_date = '1990-01-01'
        url = f'https://api.upstox.com/v2/historical-candle/{isin.replace('|','%7C')}/1minute/{today}/{start_date}'
        headers = { 'Accept': 'application/json' }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"[Error] Failed to download data. HTTP Status: {response.status_code}. May be wrong ISIN or SYMBOL.")
                return None
            
            data = response.json()  # Returns a Python dict or list
            # Save to the last file path (E:/RV/saitama/Deep_storage/Additional_storage)
            print(5)
            with open(file_paths[2], 'w', encoding='utf-8') as file:
                json.dump(data, file)
            return data
        except requests.exceptions.RequestException as e:
            print(f"[Error] Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"[Error] Downloaded data is not valid JSON: {e}")
        except Exception as e:
            print(f"[Error] Unexpected error while downloading or saving data: {e}")
    return None

   
def date_wise_list():      ### returns reversed date wise list of all previous intraday data downloaded from dadw() 
    #{"status":"success","data":{"candles":[  ["2024-12-06T15:29:00+05:30",817.55,818,817,818,75421,0],["2024-12-06T15:28:00+05:30",817.95,818,817,817.85,100533,0],["2024-12-06T15:27:00+05:30",818.3,818.35,817.5,817.95,65663,0] }
    retrieved_data = retrieve()   
    if retrieved_data == None:
        return "Data not available, or wrong ISIN or SYMBOL."
    ms=retrieved_data['data']['candles']
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
    return dc                   


def date_list(date):             # Extracting data of the given date from the list of all dates from date_wide_list()
    mc=date_wise_list()

    earliest = mc[0][0][0].split('T')[0]
    latest = mc[-1][0][0].split('T')[0]
    if date <= earliest:
        return mc[0]
    if date >= latest:
        return mc[-1]
    
    for s in range(1, len(mc)):
        current_date = mc[s][0][0].split('T')[0]
        if date < current_date:
            return mc[s - 1]
        
    #Fallback if somehow not returned in the loop
    return mc[-1]
    #date_list('2024-12-06')[0]         #        ['2024-12-06T09:15:00+05:30', 5281.45, 5366.95, 5262, 5365.9, 272932, 0]
  

#TODO date_range_list 
def date_range_list(start_date,end_date):
    import datetime
   
    from pprint import pprint
    mc=date_wise_list()



def maxfinder(date=date):              ### input date me kitna profit or loss de rha different percentage execution basis pe
    
    print(isin)
    dmc=date_list(date)
    print(dmc[0])
    print(Saraswati.percitest([l[1] for l in dmc],weight=0))




def histocast(date=date):              ### input date me kitna profit or loss de rha different percentage execution basis pe
    print(isin)

    dmc=date_list(date)
    
    input_per=0.2,0.1,0.1,0.3

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
    
    plot_x(dmc,percentage_change,inv_t,pnl,input_per)
    print(len(dmc),len(inv_t))
    


def plot_x(dmc,percentage_change,inv_t,pnl,input_per=None):
    # Plot the graph
    import matplotlib.pyplot as plt
    for i in range(0,len(percentage_change)-1):
        plt.plot([i,i+1],[percentage_change[i],percentage_change[i+1]],color="red" if inv_t[i]==-1 else "green" if inv_t[i]==1 else "blue")
    plt.text(0, 1.02, f'{dmc[0][0].split('T')[0]}'+(f'   {input_per}' if input_per!=None else '') , transform=plt.gca().transAxes, fontsize=12, color='blue')
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


def dynamic_horizon():
    lb=0
    sb=0
    ti=20  # time interval
    for n in range (0,int( len(date_list(date)) / ti ) ):
        best_per=Saraswati.percitest([l[1] for l in date_list(date)[ti*n:ti*n+ti]])[3]
        bal=Saraswati.simu([l[1] for l in date_list(date)[ti*n+ti:ti*n+2*ti]],*list(best_per)) 
        #lb=lb+bal[0]-100
        #sb=sb+
        print('long_bal(' +str(ti*n+ti) +') = ' +str(bal[0]) )
        print('short_bal(' +str(ti*n+ti) +') = ' +str(bal[1]) )
        

def faltu():
    time_int=15
    best_per=Saraswati.percitest([l[1] for l in date_list(date)[0:time_int]])[3]


if __name__ == '__main__':
    program_selection()
