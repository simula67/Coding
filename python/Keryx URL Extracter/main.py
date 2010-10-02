#!/usr/bin/python
import Debian as plug
import sys
if len(sys.argv) <= 2 :
    print "Usage :",sys.argv[0]," <keryx project directory> <packages>"
    sys.exit(1)
mydebian = plug.Debian()
arch = mydebian.loadProject(sys.argv[1])[3]
ans = raw_input("Do you want to download package list from the internet?(y/n) : ")
if ans == 'y' or ans  == 'Y' :
    internet_lst = mydebian.loadInternetPackageList(sys.argv[1],arch)
    for dl_item in internet_lst :
        print "DOWNLOAD :",dl_item[0],"TO :",dl_item[1],"AND EXPLODE TO :",dl_item[2]
        #Also explode the zip files
allPackages = mydebian.loadLocalPackageList(sys.argv[1],arch)
final_depends = []
for pack_pos in range(2,len(sys.argv)) :
    final_depends.append(mydebian.getDependencies(sys.argv[1],allPackages,sys.argv[pack_pos]))
for item1 in final_depends :
    for item2 in item1 :
        print item2[0]
