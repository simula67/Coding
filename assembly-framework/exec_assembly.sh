#!/bin/bash
#Compile the driver.c without linking
gcc -c driver.c
if [ $? -ne 0 ]; then
	echo "Compilation of driver.c unsuccessfull"
	exit 1
fi
#Now assemble
nasm -f elf skeleton.S
if [ $? -ne 0 ]; then
	echo "Assembling unsuccessful"
	exit 2
fi
#Now link
gcc -o skeleton driver.o skeleton.o
if [ $? -ne 0 ]; then
	echo "Linking unsuccessful"
	exit 3
fi
#Now execute
./skeleton
echo ""
echo "Return status was $?"
#Ask user whether to delete the compiled binary
echo -n "Do you want to delete the binary?"
read ans;
if [ $ans == y -o $ans == Y ]; then
    rm -f skeleton
    if [ $? -ne 0 ]; then
	echo "Cant delete the binary \"skeleton\""
	echo "Please delete it manually"
    fi
fi
#Cleanup
rm -f skeleton.o driver.o 
if [ $? -ne 0 ]; then
	echo "Cleanup was unsuccessful"
	echo "You may have to remove the files \"skeleton.o\" and \"driver.o\" manually"
	exit 4
fi
