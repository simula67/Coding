#ifndef FILE_BLK_H
#define FILE_BLK_H

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#ifndef NO_REG_SPACE
#define NO_REG_SPACE 1
#endif

#ifndef EMPTY_LIST
#define EMPTY_LIST 1
#endif

#define NO_SUCH_FILE 2

#define init_file_list(list) (list=NULL)

int file_errno;
typedef struct Fileblk {
  FILE *file;
  char *name;
  struct Fileblk *next;
}file_blk;

int reg_file(char *name,FILE *to_reg,file_blk **list) {
  file_blk *new_blk;
  if( (new_blk=malloc(sizeof(file_blk))) ==  NULL ) {
    fprintf(stderr,"Failed to allocate space to register new block in %s\n",__FILE__);
    file_errno=NO_REG_SPACE;
    return 1;
  }
  new_blk->file=to_reg;
  new_blk->name=name;
  new_blk->next=(*list);
  (*list)=new_blk;
  return 0;
}
FILE *ret_file(char *name,file_blk *list) {
  if(!list) {
    file_errno=EMPTY_LIST;
    return NULL;
  }
  file_blk *scan=list;
  while(scan!=NULL) {
    if(!strcmp(name,scan->name)) {
      return scan->file;
    }
    scan=scan->next;
  }
  file_errno=NO_SUCH_FILE;
  return NULL;
}
int free_file(char *name,file_blk **list) {
  file_blk *scan=(*list);
  file_blk *prev=(*list);
  if(!scan) {
    file_errno=EMPTY_LIST;
    return 1;
  }
  while(scan!=NULL) {
    if(!strcmp(scan->name,name)) {
	if(scan==prev) {
	  (*list)=(*list)->next;
	  fclose(scan->file);
	  free(scan);
	  return 0;
	}
	else {
	  prev->next=scan->next;
	  fclose(scan->file);
	  free(scan);
	  return 0;
	}
      }
      prev=scan;
      scan=scan->next;
  }
  file_errno=NO_SUCH_FILE;
  return 2;
}
int free_filelist(file_blk *list) {
  if(list==NULL) {
    file_errno=EMPTY_LIST;
    return 1;
  }
  file_blk *to_free;
  while(list!=NULL) {
    fclose(list->file);
    to_free=list;;
    list=list->next;
    free(to_free);
  }
  return 0;
}


/*Testing
 
file_blk *list;
void free_my_filelist() {
  free_filelist(list);
}
int main()
{
  init_file_list(list);
  FILE *out_file;
  atexit(free_my_filelist);
  if( (out_file=fopen("Jogy","w")) == NULL ) {
    fprintf(stderr,"Cannot open file\n");
    exit(1);
  }
  return 0;
}
*/
#endif
