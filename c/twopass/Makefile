sasm:sasm.c optab.o symtab2.o
optab.o:optab.h optab.c
	cc -c optab.c -o optab.o
symtab2.o:symtab2.h symtab2.c
	cc -c symtab2.c -o symtab2.o
clean:
	rm -f *.o
clean-all:clean
	rm -f sasm

