#include "mem_blk.h"
#include <stdio.h>
mem_blk *list;
void free_mylist() {
  free_list(list);
}
extern int mem_errorno;
int main()
{
  init_mem_list(list);
  atexit(free_mylist);
  char *name;
  if( (name=reg_memblk("Name",25,&list)) == NULL ) {
    exit(1);
  }
  printf("Enter name : ");
  fgets(name,24,stdin);
  printf("Entered name is : %s",name);
  printf("Looking for name : kuhu\n");
  if(ret_loc("kuhu",list)==NULL) {
    if(mem_errno==NO_SUCH_BLK) {
      printf("No such block\n");
    }
  }
}
