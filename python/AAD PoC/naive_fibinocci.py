#!/usr/bin/python
import sys
def fib(n):
    if(n<=2):
        return (n-1)
    else:
        return fib(n-1)+fib(n-2)
if ( len(sys.argv) == 2 ):
    print fib(int(sys.argv[1]))
else:
    print "Usage : "+sys.argv[0]+" <term required>"
    
