#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
int main(int argc,char *argv[])
{
  if(argc<2)
    {
      printf("Usage : %s <files to be removed>\n",argv[0]);
      exit(1);
    }
  int i;
  for(i=1;i<argc;i++)
    {
      //printf("Removing file : \'%s\'\n",argv[i]);
      if( unlink(argv[i]) != 0 )
	{
	  printf("File \"%s\" cannot be removed\n",argv[i]);
	}
    }
}
