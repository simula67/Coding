/*

JOSH : JOji SHell
Executes commands with no command line argument
Coded by : simula67(This is a joke, by the way)

*/
#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<stdlib.h>
const int size=50;
int main()
{
  char buff[size];
  while(1)
    {
      printf("Josh$");
      fgets(buff,(size-1),stdin);
      if(strcmp(buff,"exit\n")==0)
	break;
      else if(strcmp(buff,"help\n")==0)
	{
	  printf("\n\t\tThis is the JOji SHell\n");
	  printf("\t\tTo execute a binary just type in its full path\n");
	  printf("\t\tTo exit type \"exit\" and hit ENTER\n");
	  printf("\t\tCommand line arguments are not supported just yet\n");
	}
      else
	{
	  buff[strlen(buff)-1]='\0';
	  char *cmdln[]={buff,NULL};
	  char *env[]={NULL};
	  pid_t cmd=fork();
	  if(cmd==0)
	    {
	      execve(buff,cmdln,env);
	      printf("Execution failed\n");
	      exit(1);
	    }
	  if(cmd<0)
	    {
	      printf("Fork failed\n");
	    }
	}
      int status;
      waitpid(-1,&status,0);
    }
  return 0;
}
