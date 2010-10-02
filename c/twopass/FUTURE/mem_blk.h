#ifndef MEM_BLK_H
#define MEM_BLK_H

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define NO_BLK_SPACE 0
#define NO_REG_SPACE 1

#define EMPTY_LIST 0
#define NO_SUCH_BLK 1

#define init_mem_list(list) (list=NULL) //Initially list must be NULL

int mem_errno; //Special errno for this header
typedef struct Memblks {
  void *mem_loc;//Allocated memory
  char *name;//Name of block
  struct Memblks *next_blk;
}mem_blk;
void * reg_memblk(char *name,size_t blk_size,mem_blk ** list) { 
  //As it can be clearly seen from below the first argument must be a "const" char *
  void *alloc;
  mem_blk *new_blk;
  if( (alloc=malloc(blk_size)) == NULL ) {
    fprintf(stderr,"Failed to malloc the block in %s\n",__FILE__);
    mem_errno=NO_BLK_SPACE;//No space to allocate block
    return NULL;
  }
  if( (new_blk=malloc(sizeof(mem_blk))) == NULL ) {
    fprintf(stderr,"Failed to malloc space to register new block in %s\n",__FILE__);
    free(alloc);
    mem_errno=NO_REG_SPACE;//No space to register block
    return NULL;
  }
  new_blk->name=name;
  new_blk->mem_loc=alloc;
  new_blk->next_blk=(*list);
  (*list)=new_blk;
  return alloc;
}
void *ret_loc(char *name,mem_blk *list) {
  mem_blk *scan=list;
  if(!list) {
    mem_errno=EMPTY_LIST;//mem_errno = EMPTY_LIST whenever an operation cannot be performed due to empty list
    return NULL;
  }
  while(scan!=NULL) {
    if(!strcmp(scan->name,name)) {
      return scan->mem_loc;
    }
    scan=scan->next_blk;
  }
  mem_errno=NO_SUCH_BLK;// No such block
  return NULL;
}
int free_blk(char *name,mem_blk **list) {
  mem_blk *scan=(*list);
  mem_blk *prev=(*list);
  if(!scan) {
    mem_errno=EMPTY_LIST;
    return 1;
  }
  while(scan!=NULL) {
    if(!strcmp(scan->name,name)) {
      if(scan==prev) {
	(*list)=(*list)->next_blk;
	free(scan->mem_loc);
	free(scan);
	return 0;
      }
      else {
	prev->next_blk=scan->next_blk;
	free(scan->mem_loc);
	free(scan);
	return 0;
      }
    }
    prev=scan;
    scan=scan->next_blk;
  }
  mem_errno=NO_SUCH_BLK;
  return 2;
}
int free_list(mem_blk *list) {
  if(list==NULL) {
    mem_errno=EMPTY_LIST;
    return 1;
  }
  mem_blk *to_free;
  while(list!=NULL) {
    free(list->mem_loc);
    to_free=list;
    list=list->next_blk;
    free(to_free);
  }
  return 0;
}
#endif
