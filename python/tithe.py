#!/usr/bin/python

import sys

total = 0
for index, month in enumerate(sys.argv[1:]):
    per_month = float(month.replace(',','')) / 10
    print 'For month {} : {}'.format(index + 1, per_month)
    total += per_month

print '-' * 20
print 'TOTAL : {}'.format(total)
