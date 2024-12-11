import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Saraswati

isin='NSE_EQ|INE0ONG01011'

NOS=1

per_decrease=1/100 * 0.1

order_type="D"            ### Intraday order="I"                Delivery order="D"


def trailing_stoploss():
    import time
    td=Saraswati.time_difference()
    if td>0:
        print('sleeping for '+str(td)+' seconds')
        time.sleep(td)
    extremum=0
    while True:
        f=Saraswati.ful_mar_quo()
        ltp=f.data[next(iter(f.data))].last_price
        if ltp > extremum:
            extremum=ltp
            print('new extremum='+str(extremum))
        if ltp<extremum*(1-per_decrease):
            Saraswati.sell(order_type)
            print('sell order price='+str(ltp),'extremum='+str(extremum))
            break
        time.sleep(10)


#trailing_stoploss()


#buy()
#sell()