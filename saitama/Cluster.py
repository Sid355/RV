import Saraswati
from Historical_data_simulation import Historical_data_simulation

def edl():    #equally divided list
    dwl=Historical_data_simulation.date_wise_list()
    obs_time=10    #time interval to observe    #Note- obs_time > exe_time
    exe_time=5     #time interval to execute 
    obs_list=[]
    exe_list=[]
    for n in range(0,len(dwl)):
        for m in range(0,len(dwl[n])-obs_time-exe_time+1): #one cl_minutes is for no of interval and +1 is for list format as last exculding
            tl=dwl[n][m:m+obs_time+1]
            obs_list+=[tl]    
            sl=dwl[n][m+exe_time:m+2*exe_time+1]
            exe_list+=[sl]      
    return obs_list,exe_list

class seeder:    # seeds for cluster
    def per():
        per_change=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4]
        per_seeds=Saraswati.combination_pers()
        print(per_seeds)
        return per_seeds
    def kms(): pass

class norm:
    def l2_norm(first,second):
        first

def cluster():
    obs_list,exe_list=edl()
    seeds=seeder.per()
    



def kms_cluster(isin):                        ###it make cluster with KMean++(automatic seed points)
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






PTR=    0     # programm to run    0=nothing

if PTR==0: pass 
if PTR==1: edl()
if PTR==2: cluster()
if PTR==3: pass
if PTR==4: pass

