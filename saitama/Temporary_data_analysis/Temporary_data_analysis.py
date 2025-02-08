import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati
xs2kn=Saraswati.xs2kn

import Broker
broker=Broker.upstox


isin_quest=  2 

if isin_quest== 1 : symbol,isin= 'ITI'          ,'NSE_EQ|INE248A01017'
if isin_quest== 2 : symbol,isin= 'MOBIKWIK'     ,'NSE_EQ|INE0HLU01028'
if isin_quest== 2 : symbol,isin= 'TATAMOTORS'   ,'NSE_EQ|INE155A01022'
if isin_quest== 2 : symbol,isin= 'SWIGGY'       ,'NSE_EQ|INE00H001014'
if isin_quest== 2 : symbol,isin= 'OLAELEC'      ,'NSE_EQ|INE0LXG01040'
if isin_quest== 2 : symbol,isin= 'ADANIGREEN'   ,'NSE_EQ|INE364U01010'
if isin_quest== 2 : symbol,isin= 'ADANIPOWER'   ,'NSE_EQ|INE814H01011'
if isin_quest== 2 : symbol,isin= 'PAYTM'        ,'NSE_EQ|INE982J01020'













def intraday_maxfinder(symbol,isin):              ### input date me kitna profit or loss de rha different percentage execution basis pe
    
    data=broker.intraday_candle_data(isin)
    if data == None:
            return f"No data retrieved for ISIN: {isin}."
    
    data=data.data.candles
    data=list(reversed(data))            
    cl_price_list=[element[4] for element in data]  # only closed data list
    #print(cl_price_list)
    print(Saraswati.percitest([s for s in cl_price_list]))







if __name__ == '__main__':
        
    PTR= 1

    if PTR==0: pass
    if PTR==1: intraday_maxfinder(symbol,isin)
    if PTR==2: pass
   