if 0:
    date1='2024-06-09T09:15:00+05:30'
    date2='2024-06-17T09:15:00+05:30'

    if date1>date2: 
        print(1)
    if date2>date1: 
        print(2)
    if date2==date1: 
        print(0)

if 1:
    mc=[1,4,6,8,9,24,36,79]
    date=12
    for s in range(0,len(mc)):
        if date < mc[0]:
            date_i=0
            break
        if date < mc[s]:
            date_i=s-1
            break
    print(date_i)

if 0:
    mc=[1,4,6,8,9,24,36,79]
    for s in range(0,len(mc)):
        if mc[s]>80:
            print('Good Boy')
            print(s-1)
            break

if 0:
    mc=[1,4,6,8,9,24,36,79]
    print(mc[-1])