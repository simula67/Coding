/*
A simple copy program
Coded by simula67
*/
#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
int main(int argc,char *argv[])
{
  if(argc!=3)
    {
      printf("Usage %s <source file name> <destination FILE NAME>\n",argv[0]);
      exit(0);
    }
  FILE *source,*dest;
  source=fopen(argv[1],"rb");
  if(source==NULL)
    {
      printf("Source file open failed\n");
      exit(0);
    }
  dest=fopen(argv[2],"wb");
  if(dest==NULL)
    {
      printf("Destination file open failed\n");
      exit(0);
    }
  char ch;
  while(fread((char *)&ch,sizeof(char),1,source)!=0)
    {
      fwrite((char *)&ch,sizeof(char),1,dest);
    }
  printf("Successfully copied\n");
  fclose(source);
  fclose(dest);
}
