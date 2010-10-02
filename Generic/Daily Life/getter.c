#include<unistd.h>
#include<stdlib.h>
#include<string.h>
main()
{
char command[70];
int i;
char num[3];
/*
strcpy(command,"wget http://192.168.2.2/xampp/scene2/episode2.");
strcpy(num,"6");
int change=strlen(command);
strcat(command,num);
strcpy(command,NULL);
for(i=0;i<=9;i++)
	{
	system(command);
	command[change]++;
	}
*/
strcpy(command,"wget http://192.168.2.2/xampp/scene2/episode2.");
int change=strlen(command)+1;
strcpy(num,"10");
strcat(command,num);
strcat(command,"_xvid.avi");
for(i=0;i<=9;i++)
	{
	system(command);
	command[change]++;
	}
}
