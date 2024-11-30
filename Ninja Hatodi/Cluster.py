import Saraswati


def dt_ws_lst(isin):
    import json
    from pprint import pprint
    ms=open(Saraswati.name(isin)+'.txt','r').read()
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


print(dt_ws_lst(Saraswati.isin)[1])