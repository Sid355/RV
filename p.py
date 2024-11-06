#!/usr/bin/env python3
def p():
    ml=open("NHPC.txt").read()
    print("NHPC")
    pl=ml.split('\n')[:-1]
    ml=[float(l.split('\t')[1]) for  l in pl]
    p=0.03
    s=1
    for n in range(0,len(ml)-3):
        if (ml[n+1]-ml[n])/ml[n]<-p and (ml[n+2]-ml[n+1])/ml[n+1]<-p:
            g=(ml[n+3]-ml[n+2])/ml[n+2]
            if 0:
                s*=(1.0+g)
            else:
                s+=g
            print(n,g*100)
    print((s-1)*100)

def d():
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/NSE_EQ%7CINE745G01035/1minute/2024-11-13/2023-11-12'
    headers = {
    'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    open('mcx.txt','w').write(response.text)
def tkp():
    import requests
    url = 'https://api.upstox.com/v2/historical-candle/intraday/NSE_EQ%7CINE745G01035/1minute'
    headers = {
                'Accept': 'application/json'
                }
    response = requests.get(url, headers=headers)
    return response.text
def t():
    import json
    from pprint import pprint
    nl=open('mcx.txt','r').read()
    tk=tkp()
    nl=json.loads(tk)['data']['candles']+json.loads(nl)['data']['candles']
    print(tk)
    ns=[]
    pks=[]
    vps=[]
    for n in range(0,len(nl)):
        k=[int(s) for s in nl[n][0].split('T')[1].split('+')[0].split(':')]
        if 0 and len(pks)==ppvs:
            ns+=[pks]
            vps+=[nl[n-1+vpsk][1]]
            pks=[]
        if 0 and len(pks)<15 and ((len(pks)!=0) or k[0]<14):
            pks+=[nl[n][1]]
        if k[0]==9 and k[1]<=30:
            pks+=[nl[n][1]]
        elif pks!=[]:
            ns+=[pks]
            vps+=[nl[n+30][1]]
            pks=[]
    for n in range(0,len(ns)):
        s=0
        for ps in range(0,len(ns[n])):
            s+=ns[n][ps]
        s/=len(ns[n])
        vps[n]=(vps[n]-ns[n][-1])/ns[n][-1]
        for ps in range(0,len(ns[n])):
            ns[n][ps]=(ns[n][ps]-s)/s
    from sklearn.cluster import KMeans
    import numpy as np
    ns=np.array(ns)
    vss=5
    vk=KMeans(n_clusters=vss,random_state=0,n_init="auto").fit(ns)
    vks=vk.predict(ns)
    print(vks)
    svvs=[0]*vss
    pvs=[0]*vss
    for n in range(0,len(vks)):
        svvs[vks[n]]+=vps[n]
        pvs[vks[n]]+=1
    for n in range(0,vss):
        svvs[n]/=pvs[n]
    print(svvs,pvs)
    import matplotlib.pyplot as plt
    for k in range(0,vss):
        plt.figure(k)
        for n in range(0,len(vks)):
            if vks[n]==k:
                plt.plot(ns[n])
    if 0:plt.show()
def c():
    import json
    from pprint import pprint
    nl=open('mcx.txt','r').read()
    tk=tkp()
    nl=json.loads(tk)['data']['candles']+json.loads(nl)['data']['candles']
    print(tk)
    ns=[]
    pks=[]
    vps=[]
    from termcolor import colored
    for n in range(0,len(nl)):
        k=[int(s) for s in nl[n][0].split('T')[1].split('+')[0].split(':')] # hour k[0] minute k[1] open nl[n][1] high [n][2] low [n][3] close [n][4] volume [n][5] Open Interest [n][6]
        pv=(nl[n][4]-nl[n][1])/nl[n][1]
        if k[0]==9 and k[1]==15:print('\n')
        print(colored(min(abs(int(pv*1000)),9),'red' if pv<0 else 'green'),end='')
        
c()
