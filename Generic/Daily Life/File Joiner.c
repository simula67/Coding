#include<stdio.h>
#include<string.h>
main()
{
FILE *inp;
FILE *out;
out=fopen("Spider.mkv","wb");
char inpfilename[]="Spider_www.tinyrip.info_.mkv.001";
int i,len;
len=strlen(inpfilename);
len--;
char ch;
for(i=1;i<=6;i++)
	{
	inp=fopen(inpfilename,"rb");
	while(fread(&ch,sizeof(char),1,inp)==1)
	{
		fwrite(&ch,sizeof(char),1,out);

	}
	fclose(inp);	
	inpfilename[len]++;
	}
}
