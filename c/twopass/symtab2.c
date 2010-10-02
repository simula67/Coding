#ifndef _SYMTAB2_H
#define _SYMTAB2_H
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"symtab2.h"
#define SIZE 10

typedef struct Sym_node
{
  char *label;
  long int val;
}sym_node;

typedef struct Sym_coll
{
  sym_node *node;
  struct Sym_coll *next;
}sym_coll;
typedef struct Sym_tab
{
  sym_coll *first;
  struct Sym_tab *next;
}sym_tab;

unsigned int hashfunc(char* key)
{
  int i=0;
  size_t len,asciisum=0;
  unsigned int hash;
  len=strlen(key);
  for(;i<len;i++)
    {
      asciisum+=key[i];
    }
  hash=asciisum%SIZE;
  return hash;
}


int insert_symtab(char *key,sym_tab *symtab,long int addr)
{
  unsigned int loc=hashfunc(key);
  while(loc)
    {
      symtab=symtab->next;
      loc--;
    }
  if(symtab->first==NULL)
    {
      symtab->first=malloc(sizeof(sym_coll));
      if(symtab->first==NULL)
	{
	  printf("Out of memmory\n");
	  return 1;
	}
      memset(symtab->first,0,sizeof(sym_coll));
      if( (symtab->first->node=malloc(sizeof(sym_node)))==NULL )
	{
	  printf("Out of memory\n");
	  symtab->first->next=NULL;
	  return 1;
	}
      memset(symtab->first->node,0,sizeof(sym_node));
      if( (symtab->first->node->label=malloc(strlen(key)+1))==NULL )
	{
	  printf("Out of memory\n");
	  return 1;
	}
      strcpy(symtab->first->node->label,key);
      symtab->first->node->val=addr;
      symtab->first->next=NULL;
    }
  else
    {
      sym_coll *insert;
      for(insert=symtab->first;insert->next!=NULL;insert=insert->next);
      if( (insert->next=malloc(sizeof(sym_coll)))==NULL )
	{
	  printf("Out of memory\n");
	  return 1;
	}
      memset(insert->next,0,sizeof(sym_coll));
      if( (insert->next->node=malloc(sizeof(sym_node)))==NULL )
	{
	  printf("Out of memory\n");
	  insert->next->next=NULL;
	  return 1;
	}
      memset(insert->next->node,0,sizeof(sym_node));
      if( (insert->next->node->label=malloc(strlen(key)+1))==NULL )
	{
	  printf("Out of memory\n");
	  return 1;
	}
      strcpy(insert->next->node->label,key);
      insert->next->node->val=addr;
      insert->next->next=NULL;
    }
  return 0;
}
void free_symtab(sym_tab *symtab)
{
  sym_tab *tab_free;
  sym_coll *coll_free,*coll_scan;
  while(symtab!=NULL)
    {
      coll_scan=symtab->first;
      while(coll_scan!=NULL)
	{
	  free(coll_scan->node->label);
	  free(coll_scan->node);
	  coll_free=coll_scan;
	  coll_scan=coll_scan->next;
	  free(coll_free);
	}
      tab_free=symtab;
      symtab=symtab->next;
      free(tab_free);
    }
}

sym_tab * init_symtab(void)
{
  sym_tab *symtab;
  int i;
  sym_tab *gen;
  symtab=(sym_tab *)malloc(sizeof(symtab));
  if(symtab==NULL)
    return NULL;
  memset(symtab,0,sizeof(sym_tab));
  for(i=0,gen=symtab;i<SIZE;i++,gen=gen->next)
    {
      if( (gen->next=(sym_tab *)malloc(sizeof(symtab)))==NULL )
	{
	  printf("Out of memory\n");
	  free_symtab(symtab);
	  return NULL;
	}
      memset(gen->next,0,sizeof(sym_tab));
    }
  return symtab;
}
#define INVALID_SYMTAB -1
#define NOT_FOUND -2

long int search_symtab(sym_tab *symtab,char *label)
{
  unsigned int loc=hashfunc(label);
  if(symtab==NULL)
    {
      printf("Invalid symtab\n");
      return INVALID_SYMTAB;
    }
  while(loc)
    {
      symtab=symtab->next;
      loc--;
    }
  sym_coll *scan;
  for(scan=symtab->first;scan!=NULL;scan=scan->next)
    {
      if(strcmp(scan->node->label,label)==0)
	return scan->node->val;
    }
  return NOT_FOUND;
}
/*
 * 
 * Testing 
 * 
 * 
int main(int argc,char *argv[])
{
  sym_tab  *symtab;
  if( (symtab=init_symtab())==NULL )
    {
      printf("Failed to initiate symtab\n");
      return 1;
    }
  int choice;
  char inp_label[26];
  long int addr;
  do
    {
      printf("MENU\n");
      printf("1.Enter values into symtab\n");
      printf("2.Search in symtab\n");
      printf("3.Exit\n");
      printf("Please enter your choice : ");
      scanf("%d",&choice);
      switch(choice)
	{
	case 1:
	  printf("Enter the label(MAX 25) characters : ");
	  getc(stdin);
	  fgets(inp_label,25,stdin);
	  inp_label[(strlen(inp_label)-1)]='\0';
	  printf("Enter the address : ");
	  scanf("%ld",&addr);
	  if(insert_symtab(inp_label,symtab,addr)!=0)
	    {
	      printf("Error inserting\n");
	    }
	  break;
	case 2:
	  printf("Enter label to search : ");
	  getc(stdin);
	  fgets(inp_label,25,stdin);
	  inp_label[(strlen(inp_label)-1)]='\0';
	  if( (addr=search_symtab(symtab,inp_label))<0 )
	    {
	      printf("Symbol Not Found\n");
	    }
	  else
	    {
	      printf("The value for the label %s is : %ld\n",inp_label,addr);
	    }
	  break;
	case 3:
	  free_symtab(symtab);
	  break;
	default:
	  printf("Invalid choice...\n");
	  printf("Please enter again...\n");
	}
    }while(choice!=3);
}
*
* 
* 
*/

#endif
