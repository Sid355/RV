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
d()
