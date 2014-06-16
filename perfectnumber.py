from math import sqrt
n = int(raw_input('input a number:'))
sum = 0
for i in range(1,n/2+1):
    print i
    if n%i == 0:
        sum += i
    print 'sum %d,i %d'%(sum,i)
if sum == n:
    print 'YES'
else:
    print 'NO'
