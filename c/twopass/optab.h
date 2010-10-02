/*
WARNING: THE RETURN VALUE OF OPTAB LOADING MUST BE CHECKED BEFORE USING THE OPTAB. PASSING INCORRECT OPTABS FOR SEARCHING OR FREEING WILL MOST CERTAINLY LEAD TO SEGMENTATION FAULTS. IF IT DOES NOT GIVE SEGMENTATION FAULTS, THE PROGRAM MAY BEHAVE VERY WIERDLY. YOU HAVE BEEN WARNED.

The file containing pneumonic-opcode pairs must be of the form:
<pneumonic1>=<opcode>\n
<pneumonic2>=<opcode>\n
...
The newline is absolutely necessary at the end of each pneumonic declaration.
Coded by : simula67
*/
#ifndef _OPTAB_H
#define _OPTAB_H
extern void free_optab(char ***optab,int num_ops);
extern char *** load_optab(char *filename,int *num_ops);
extern char * search_optab(char ***optab,char * neum,int num_ops);

#endif
