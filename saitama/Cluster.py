import Saraswati


def dt_ws_lst(isin):             ### it will make a date wise list of any given list
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

def obsv_wndw(isin):             ## The time period we will observe
    dwl=dt_ws_lst(isin)
    last_exclude=5
    window_size=5   ## no of point
    neo_list=[]
    for k in range(0,len(dwl)):
        for s in range(0,len(dwl[k])-last_exclude) :
            tl=[l[4] for l in dwl[k][s:s+window_size]]  #s+ ka last wala include nehni hota     
            neo_list+= [[(tl[q+1]-tl[q])/tl[q]*100 for q in range(0,window_size-1)]]   
    return neo_list

def cluster(isin):                        ###it make cluster with KMean++(automatic seed points)
    from sklearn.cluster import KMeans
    import numpy as np
    ns=obsv_wndw(isin)
    ns=np.array(ns)
    vss=5                                                                 ## no of clusters
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
                plt.plot(np.concatenate((ns[n],np.array(nstd[n])[0:1])))
    if 1:plt.show()


print(obsv_wndw(Saraswati.isin))
#print(dt_ws_lst(Saraswati.isin)[1])%%