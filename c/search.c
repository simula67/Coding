#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
main(int argc,char *argv[])
{
if(argc!=2)
	{
	printf("Too few or too many arguments...\n");
	exit(0);
	}
if(strlen(argv[1])!=10)
	{
	printf("Incorrect form for phone number");
	printf("\nPlease enter the phone number in 10 digits");
	printf(" without country code\n");
	exit(0); 
	}
char command[90000]="grep ";
strcat(command,argv[1]);
strcat(command," /media/DATAPART1/My\\ 5610/Contacts/");
FILE *fp;
if((fp=fopen("list.txt","r"))==NULL)
	{
	printf("\nError opening a file\n");
	exit(0);
	}

char ch;
char temp_str[5];
while((ch=fgetc(fp))!=EOF)
	{

	if(isalpha(ch)||ch=='.'||ch=='_'||ch=='-')
		{
		temp_str[0]=ch;
		temp_str[1]='\0';
		strcat(command,temp_str);
		}
	else if(ch==' ')
		{
		temp_str[0]='\\';
		temp_str[1]=' ';
		temp_str[2]='\0';
		strcat(command,temp_str);
		}
	else if(ch=='\n')
		{
		strcat(command," /media/DATAPART1/My\\ 5610/Contacts/");
		}
	}
system(command);
fclose(fp);
}
