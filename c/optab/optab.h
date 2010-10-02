/*
WARNING: THE RETURN VALUE OF OPTAB LOADING MUST BE CHECKED BEFORE USING THE OPTAB. PASSING INCORRECT OPTABS FOR SEARCHING OR FREEING WILL MOST CERTAINLY LEAD TO SEGMENTATION FAULTS. IF IT DOES NOT GIVE SEGMENTATION FAULTS, THE PROGRAM MAY BEHAVE VERY WIERDLY. YOU HAVE BEEN WARNED.

The file containing pneumonic-opcode pairs must be of the form:
<pneumonic1>=<opcode>\n
<pneumonic2>=<opcode>\n
...
The newline is absolutely necessary at the end of each pneumonic declaration.
Coded by : simula67
*/
#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<stdlib.h>
void free_optab(char ***optab,int num_ops)
{
  while(num_ops>0)
    {
      num_ops--;
      free(optab[0][num_ops]);
      free(optab[1][num_ops]);
    }
  free(optab[0]);
  free(optab[1]);
  free(optab);
}
/*The following function is invoked if optab generation fails when the opfile is processed line-by-line*/
static void gar_coll(char ***optab,int curr_op,int right)
{
  int i;
  for(i=0;i<curr_op;i++)
    {
      free(optab[0][i]);
      free(optab[1][i]);
    }
  if(right)
    free(optab[0][i]);
}
char *** load_optab(char *filename,int *num_ops)
{
  char ***optab;
  FILE *opfile;
  if( (opfile=fopen(filename,"r")) ==  NULL )
    {
      fprintf(stderr,"Opfile open failed...\n");
      return 0;
    }
  int ch;
  /*Let us find out how many pneumonic-opcode pairs are in the file*/
  *num_ops=0;
  while( (ch=fgetc(opfile)) != EOF )
    if(ch=='\n')
      (*num_ops)++;
  fclose(opfile);
  /*Here we try to allocate memory for first two dimensions of optab*/
  if( (optab=malloc(2*sizeof(char ***))) == NULL )//Two rows : one each for pneumonics and opcodes
    {  
      fprintf(stderr,"Out of memmory\n");
      return 0;
    }
  if((optab[0]=malloc((*num_ops)*sizeof(char **)))==NULL)
    {
      free(optab);
      fprintf(stderr,"Out of memmory\n");
      return 0;
    }
  if((optab[1]=malloc((*num_ops)*sizeof(char **)))==NULL)
    {
      free(optab[0]);
      free(optab);
      fprintf(stderr,"Out of memmory\n");
      return 0;
    }
  if( (opfile=fopen(filename,"r")) ==  NULL )
    {
      free_optab(optab,0);
      fprintf(stderr,"Opfile open failed...\n");
      return 0;
    }
  char *buff=NULL;
  size_t len=0;
  ssize_t read;
  int curr_op=0,i;
  while((read=getline(&buff,&len,opfile)) != -1)
    {
      if(curr_op>=*num_ops)
	{
	  free_optab(optab,*num_ops);
	  fprintf(stderr,"Trailing newline missing...\n");
	  return 0;
	}
      for(i=0;buff[i]!='=';i++)
	{
	  if(buff[i]=='\0')
	    {
	      gar_coll(optab,curr_op,0);
	      fprintf(stderr,"Your specified opfile is not valid...\n");
	      return 0;
	    }
	}
      if( (optab[0][curr_op]=malloc((i+1)*sizeof(char))) == NULL )
	{
	  gar_coll(optab,curr_op,0);
	  fprintf(stderr,"Out of memmory\n");
	  return 0;
	} 
      strncpy(optab[0][curr_op],buff,i);
      optab[0][curr_op][i]='\0';
      char *opcd=buff+i+1;
      if(opcd[0]=='\n')
	{
	  gar_coll(optab,curr_op,1);
	  fprintf(stderr,"Your specified opfile is not valid...\n");
	  return 0;
	}
      if( (optab[1][curr_op]=malloc((strlen(opcd))*sizeof(char))) == NULL )
	{
	  gar_coll(optab,curr_op,1);
	  fprintf(stderr,"Out of memmory\n");
	  return 0;
	} 
      for(i=0;opcd[i]!='\n';i++)
	{
	  optab[1][curr_op][i]=opcd[i];
	}	  
      optab[1][curr_op][i]='\0';
      curr_op++;
      free(buff);
      buff=NULL;
    }
  return optab;
}
char * search_optab(char ***optab,char * neum,int num_ops)
{
  int i;
  for(i=0;i<num_ops;i++)
    {
      if(strcmp(optab[0][i],neum)==0)
	return optab[1][i];
    }
  return NULL;
}

