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
def t():
    import json
    from pprint import pprint
    nl=open('mcx.txt','r').read()
    nl=json.loads(nl)['data']['candles']
    ns=[]
    pks=[]
    vps=[]
    for n in range(0,len(nl)):
        k=[int(s) for s in nl[n][0].split('T')[1].split('+')[0].split(':')]
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
    svvs=[0]*vss
    pvs=[0]*vss
    for n in range(0,len(vks)):
        svvs[vks[n]]+=vps[n]/vss
        pvs[vks[n]]+=1
    print(svvs,pvs)
    import matplotlib.pyplot as plt
    for k in range(0,vss):
        plt.figure(k)
        for n in range(0,len(vks)):
            if vks[n]==k:
                plt.plot(ns[n])
    plt.show()
t()
