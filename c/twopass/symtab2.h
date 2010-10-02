#ifndef _SYMTAB2_H
#define _SYMTAB2_H
typedef struct Sym_node sym_node;
typedef struct Sym_coll sym_coll;
typedef struct Sym_tab sym_tab;
extern int insert_symtab(char *key,sym_tab *symtab,long int addr);
extern void free_symtab(sym_tab *symtab);
extern sym_tab * init_symtab(void);
extern long int search_symtab(sym_tab *symtab,char *label);

#endif
