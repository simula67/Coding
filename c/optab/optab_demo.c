#include<stdio.h>
#include"optab.h"


int main(int argc,char *argv[])
{
  char ***optab=NULL;
  int num_ops;
  if(argc!=2)
    {
      printf("Usage : %s <opfile>\n",argv[0]);
      exit(1);
    }
  if( (optab=load_optab(argv[1],&num_ops)) == NULL)
    {
      printf("Optab generation failed\n");
      exit(1);
    }
  char inp[25];
  char *res;
  while(1)
    {
      printf("Enter pneumonic(ENTER to terminate) : ");
      fgets(inp,24,stdin);
      inp[strlen(inp)-1]='\0';
      if(strcmp(inp,"")==0)
	break;
      res=search_optab(optab,inp,num_ops);
      if(res == NULL)
	{
	  printf("Pneumonic not found in optab\n");
	}
      else
	{
	  printf("Opcode is : %s\n",res);
	}
    }  
  free_optab(optab,num_ops);
  return 0;
}
