#!/usr/bin/python
import sys
def fib_rec(n,fibn):
    if(n<=1):
        return n
    if(fibn[n-1]>0):
        return fibn[n-1]
    else:
        fibn[n-1] = fib_rec(n-1,fibn) + fib_rec(n-2,fibn)
        return fibn[n-1]
def fib(n):
    n = n-1
    fibn = []
    for i in range(0,n):
        fibn.append(-1)
    return fib_rec(n,fibn)
if ( len(sys.argv) == 2 ):
    print fib(int(sys.argv[1]))
else:
    print "Usage : "+sys.argv[0]+" <term required>"
    
