#include<stdio.h>
#include<string.h>
main()
{
FILE *inp;
FILE *out;
out=fopen("Hackers.part1","wb");
inp=fopen("/media/DATAPART1/Multimedia/Movies/English/Jogy/Hackers_2-Operation_Takedown.avi","rb");
char ch;
unsigned long SIZE=141557760;
unsigned long i;
for(i=0;i<=SIZE;i++)
	{
	fread(&ch,sizeof(char),1,inp);
	fwrite(&ch,sizeof(char),1,out);
	}
fclose(out);
out=fopen("Hackers.part2","wb");
while(fread(&ch,sizeof(char),1,inp)==1)
	{
		fwrite(&ch,sizeof(char),1,out);

	}
fclose(out);
fclose(inp);
}
