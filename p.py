ml=open("ml.txt").read()
ml=[float(l.split('\t')[1]) for  l in ml.split('\n')[:-1]]
p=0.01
for n in range(0,len(ml)-4):
    if (ml[n+1]-ml[n])/ml[n]<-p and (ml[n+2]-ml[n+1])/ml[n+1]<-p and (ml[n+3]-ml[n+2])/ml[n+2]<-p:
        print(n,(ml[n+4]-ml[n+3])/ml[n+3]*100)
        
