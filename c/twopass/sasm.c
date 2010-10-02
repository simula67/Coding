#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include"optab.h"
#include"symtab2.h"
#define MC_SIZE 100
char mc[MC_SIZE];
void convert_const(char **operand_ptr)
{
  char *operand=(*operand_ptr);
  char *last;
  int i=0;
  long int val;
  memset(mc,0,MC_SIZE);
  if( ((*operand) == 'x')|| ((*operand) == 'X') )
    {
      operand+=2;
      while((*operand)!='\'')
	{
	  sprintf(mc+i,"%C",*operand);
	  mc[i]=toupper(mc[i]);
	  operand++;
	  i++;
	}
    }
  else
    {
      operand+=2;
      while((*operand)!='\'')
	{
	  sprintf(mc+i,"%02X",*operand);
	  operand++;
	  i+=2;
	}
    }
}
void decode(char *read_line,ssize_t read_len,char **label,char **pneumonic,char **operand,char *int_filename,FILE *inp_file,FILE *int_file,FILE *out_file,char ***optab,int num_ops,sym_tab *symtab,long int LOCCTR,char *read_raw_line)
{
  (*label)=NULL;
  (*pneumonic)=NULL;
  (*operand)=NULL;
  char *work_string;
  if( (work_string=malloc(read_len+1)) == NULL )
    {
      printf("Out of memory\n");
      if(inp_file)
	fclose(inp_file);
      if(int_file)
	fclose(int_file);
      if(out_file)
	fclose(out_file);
      if(int_filename)
	free(int_filename);
      if(read_raw_line)
	free(read_raw_line);
      else
	free(read_line);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(12);
    }
  sscanf(read_line,"%s",work_string);
  if( work_string[strlen(work_string)-1] == ':' )
    (*label)=work_string;
  else
    free(work_string);
  work_string=NULL;
  if( (work_string=malloc(read_len+1)) == NULL )
    {
      printf("Out of memory\n");
      if(inp_file)
	fclose(inp_file);
      if(int_file)
	fclose(int_file);
      if(out_file)
	fclose(out_file);
      if(int_filename)
	free(int_filename);
      if(read_raw_line)
	free(read_raw_line);
      else
	free(read_line);
      if((*pneumonic))
	free((*pneumonic));
      else
	free((*label));
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(12);
    }
  if((*label))
    {
      strcpy(work_string,"");
      sscanf(strstr(read_line,(*label))+strlen((*label)),"%s",work_string);
      if((*work_string)=='\0')
	{
	  printf("Bad Assembly coding...\n");
	  printf("No peumonic corresponding to label at %lX\n",LOCCTR);
	  if(inp_file)
	    fclose(inp_file);
	  if(int_file)
	    fclose(int_file);
	  if(out_file)
	    fclose(out_file);
	  if(int_filename)
	    free(int_filename);
	  if(read_raw_line)
	    free(read_raw_line);
	  else
	    free(read_line);
	  free((*label));
	  free(work_string);
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(12);
	}
      (*pneumonic)=work_string;
      work_string=NULL;
      if( (work_string=malloc(read_len+1)) == NULL )
	{
	  printf("Out of memory\n");
	  if(inp_file)
	    fclose(inp_file);
	  if(int_file)
	    fclose(int_file);
	  if(out_file)
	    fclose(out_file);
	  if(int_filename)
	    free(int_filename);
	  if(read_raw_line)
	    free(read_raw_line);
	  else
	    free(read_line);
	  free((*label));
	  free((*pneumonic));
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(14);
	}
      strcpy(work_string,"");
      sscanf(strstr(read_line,(*pneumonic))+strlen((*pneumonic)),"%s",work_string);
      if((*work_string)!='\0')
	(*operand)=work_string;
      else
	free(work_string);
    }
  else
    {
      sscanf(read_line,"%s",work_string);
      (*pneumonic)=work_string;
      work_string=NULL;
      if( (work_string=malloc(read_len+1)) == NULL )
	{
	  printf("Out of memory\n");
	  if(inp_file)
	    fclose(inp_file);
	  if(int_file)
	    fclose(int_file);
	  if(out_file)
	    fclose(out_file);
	  if(int_filename)
	    free(int_filename);
	  if(read_raw_line)
	    free(read_raw_line);
	  else
	    free(read_line);
	  free((*pneumonic));
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(14);
	}
      strcpy(work_string,"");
      sscanf(strstr(read_line,(*pneumonic))+strlen((*pneumonic)),"%s",work_string);
      if((*work_string)=='\0')
	free(work_string);
      else
	{
	  (*operand)=work_string;
	  work_string=NULL;
	}
    }
}
int main(int argc,char *argv[])
{
  if(argc!=2)
    {
      printf("Usage: %s <input file>\n",argv[0]);
      exit(1);
    }  
  /* Load Optab */
  char ***optab=NULL;
  int num_ops;
  if( (optab=load_optab("opfile",&num_ops)) == NULL)
    {
      printf("Optab generation failed\n");
      exit(2);
    }
  /* Now let us load and initialize the symtab */
  sym_tab  *symtab=NULL;
  if( (symtab=init_symtab())==NULL )
    {
      printf("Failed to initiate symtab\n");
      free_optab(optab,num_ops);
      exit(3);
    }
  FILE *inp_file=NULL;
  if( (inp_file=fopen(argv[1],"r")) == NULL )
    {
      printf("Failed to open input file\n");
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(4);
    }
  FILE *out_file=NULL;
  char *int_filename=NULL;
  if( (int_filename=(char *)malloc(strlen(argv[1])+5)) == NULL )
    {
      printf("Out of memory\n");
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(5);
    }
  strcpy(int_filename,argv[1]);
  strcat(int_filename,"_INT");
  FILE *int_file=NULL;
  if( (int_file=fopen(int_filename,"w+")) == NULL )
    {
      printf("Failed to open intermediate file\n");
      free_optab(optab,num_ops);
      free_symtab(symtab);
      free(int_filename);
      fclose(inp_file);
      exit(6);
    }
  /* And Here We Go */
  long int LOCCTR=0;
  long int start_addr;
  char *read_line=NULL;
  size_t to_read = 0;
  ssize_t read_len;
  char *work_string=NULL;
  char *work_string2=NULL;
  char *prog_name=NULL;
  char *search_space=NULL;
  int start_loop=0;
  while( (read_len=getline(&read_line,&to_read,inp_file)) != -1 )
    {
      if( (search_space=(char *)malloc(read_len+1)) == NULL )
	{
	  printf("Out of memory\n");
	  fclose(inp_file);
	  fclose(int_file);
	  free(int_filename);
	  free(read_line);
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(10);
	}
      strcpy(search_space,"");
      sscanf(read_line,"%s",search_space);
      if(((*search_space)=='\0')||((*search_space)==';'))
	{
	  free(search_space);
	  search_space=NULL;
	  free(read_line);
	  read_line=NULL;
	  continue;
	}
      free(search_space);
      search_space=NULL;
      if( (prog_name=malloc(read_len+1)) == NULL )
	{
	  printf("Out of memory\n");
	  fclose(inp_file);
	  fclose(int_file);
	  free(int_filename);
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(7);
	}

      if( (work_string=malloc( (read_len-strlen(prog_name)) +1) ) == NULL) 
	{
	  printf("Out of memory\n");
	  fclose(inp_file);
	  fclose(int_file);
	  free(prog_name);
	  free(int_filename);
	  free_optab(optab,num_ops);
	  free_symtab(symtab);
	  exit(7);
	}
      sscanf(read_line,"%s%s",prog_name,work_string);
      if(!strcmp(work_string,"START"))
	{
	  if( (work_string2=malloc((read_len-strlen(work_string))+1)) == NULL )
	    {
	      free(work_string);
	      free(prog_name);
	      fclose(inp_file);
	      fclose(int_file);
	      free(int_filename);
	      free_optab(optab,num_ops);
	      free_symtab(symtab);
	      printf("Out of memory\n");
	      exit(8);
	    }
	  char *searched=strstr(read_line,work_string);
	  sscanf(searched+strlen(work_string),"%s",work_string2);
	  if((*work_string2)=='\0')
	    {
	      printf("START directive requires an argument\n");
	      free(work_string);
	      free(prog_name);
	      free(work_string2);
	      fclose(inp_file);
	      fclose(int_file);
	      free(int_filename);
	      free_optab(optab,num_ops);
	      free_symtab(symtab);
	      exit(9);
	    }
	  char *waste;
	  LOCCTR=strtol(work_string2,&waste,16);
	  if(waste == work_string2)
	    {
	      printf("Bad Assembly coding...\n");
	      printf("No suitable value for operand for START directive\n");
	      free(work_string);
	      free(prog_name);
	      free(work_string2);
	      fclose(inp_file);
	      fclose(int_file);
	      free(int_filename);
	      free_optab(optab,num_ops);
	      free_symtab(symtab);
	      exit(9);
	    }
	  start_addr=LOCCTR;
	  fprintf(int_file,"%lX\t%s\t%s\t%lX\n",LOCCTR,prog_name,work_string,start_addr);
	  free(work_string2);
	  free(prog_name);
	  prog_name=NULL;
	  free(work_string);
	  work_string=NULL;
	  free(read_line);
	  read_line=NULL;
	  to_read=0;
	  while( (read_len=getline(&read_line,&to_read,inp_file)) != -1) 
	    {
	      if( (search_space=(char *)malloc(read_len+1)) == NULL )
		{
		  printf("Out of memory\n");
		  fclose(inp_file);
		  fclose(int_file);
		  free(int_filename);
		  free(read_line);
		  free_optab(optab,num_ops);
		  free_symtab(symtab);
		  exit(10);
		}
	      strcpy(search_space,"");
	      sscanf(read_line,"%s",search_space);
	      if(((*search_space)=='\0')||((*search_space)==';'))
		{
		  free(search_space);
		  search_space=NULL;
		  free(read_line);
		  read_line=NULL;
		  continue;
		}
	      free(search_space);
	      search_space=NULL;
	      break;
	    }
	  start_loop=1;
	}
      else
	{
	  LOCCTR=start_addr=0;
	  start_loop=1;
	}
      if(start_loop)
	break;
    }
  // Check if the loop exited becuase the EOF was reached. If so exit...
  if(read_len == -1)
    {
      if(read_line)
	free(read_line);
      fclose(inp_file);
      fclose(int_file);
      free(int_filename);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(0);
    }
  if( (work_string=malloc(read_len+1)) == NULL )
    {
      printf("Out of memory\n");
      fclose(inp_file);
      fclose(int_file);
      free(int_filename);
      free(read_line);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(11);
    }
  char *label=NULL;
  char *pneumonic=NULL;
  char *operand=NULL;
  decode(read_line,read_len,&label,&pneumonic,&operand,int_filename,inp_file,int_file,NULL,optab,num_ops,symtab,LOCCTR,NULL);
  if(label)
    label[strlen(label)-1]='\0';
  while(strcmp(pneumonic,"END"))
    {
      if(label)
	fprintf(int_file,"%lX\t%s\t%s\t%s\n",LOCCTR,label,pneumonic,operand);
      else
	{
	  if(operand)
	    fprintf(int_file,"%lX\t%s\t%s\n",LOCCTR,pneumonic,operand);
	  else
	    fprintf(int_file,"%lX\t%s\n",LOCCTR,pneumonic);
	}

      if(label)
	{
	  label[strlen(label)-1]='\0';
	  if(search_symtab(symtab,label)>0)
	    {
	      printf("Duplicate symbol at %lX\n",LOCCTR);
	      fclose(inp_file);
	      fclose(int_file);
	      free(int_filename);
	      free(read_line);
	      if(label)
		free(label);
	      if(operand)
		free(operand);
	      if(pneumonic)
		free(pneumonic);
	      free_optab(optab,num_ops);
	      free_symtab(symtab);
	      exit(12);
	    }
	  else
	    {
	      if(insert_symtab(label,symtab,LOCCTR)!=0)
		{
		  printf("Failed to insert into symtab\n");
		  fclose(inp_file);
		  fclose(int_file);
		  free(int_filename);
		  free(read_line);
		  if(label)
		    free(label);
		  if(operand)
		  free(operand);
		  if(pneumonic)
		    free(pneumonic);
		  free_optab(optab,num_ops);
		  free_symtab(symtab);
		  exit(13);
		}
	    }
	}
      char *opcode,*waste;
      if( (opcode=search_optab(optab,pneumonic,num_ops)) != NULL)
	{
	  LOCCTR+=3;
	}
      else if(!strcmp(pneumonic,"WORD"))
	{
	  LOCCTR+=3;
	}
      else if(!strcmp(pneumonic,"RESW"))
      {
	if(operand == NULL)
	  {
	    printf("Bad assembly coding...\n");
	    printf("No value given for operand near RESW directive at %lX\n",LOCCTR);
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(23);
	    
	  }
	else
	  {
	    LOCCTR+=(3*strtol(operand,&waste,10));
	    if(waste == operand)
	      {
		printf("Bad assembly coding...\n");
		printf("No suitable value was found for allocating memory for RESW directive at %lX\n",LOCCTR);
		fclose(inp_file);
		fclose(int_file);
		free(int_filename);
		free(read_line);
		if(label)
		  free(label);
		if(operand)
		  free(operand);
		if(pneumonic)
		  free(pneumonic);
		free_optab(optab,num_ops);
		free_symtab(symtab);
		exit(21);
	      }
	  }
      }
    else if(!strcmp(pneumonic,"RESB"))
      {
	if(operand == NULL)
	  {
	    printf("Bad assembly coding...\n");
	    printf("No value given for operand near RESB directive at %lX\n",LOCCTR);
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(23);
	      
	
	  }
	else
	  {
	    LOCCTR+=(strtol(operand,&waste,10));
	    if(waste == operand)
	      {
		printf("Bad assembly coding...\n");
		printf("No suitable value was found for allocating memory for RESB directive at %lX\n",LOCCTR);
		fclose(inp_file);
		fclose(int_file);
		free(int_filename);
		free(read_line);
		if(label)
		  free(label);
		if(operand)
		  free(operand);
		if(pneumonic)
		  free(pneumonic);
		free_optab(optab,num_ops);
		free_symtab(symtab);
		exit(22);
	      }
	  }
      }
    else if(!strcmp(pneumonic,"BYTE"))
      {
	long int old_locctr=LOCCTR;
	if(!operand)
	  {
	    printf("Bad assembly coding...\n");
	    printf("No operand corresponding to BYTE directive at %lX\n",LOCCTR);
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(52);
	  }
	if( ((*operand)=='c')|| ((*operand)=='C'))
	  LOCCTR+=(strlen(operand)-3);
	else if( ((*operand)=='x')|| ((*operand)=='X'))
	  {
	    LOCCTR+=(strlen(operand)-3)/2;
	    if( (strlen(operand)-3)%2)
	      LOCCTR+=1;
	  }
	else
	  {
	    printf("Bad assembly coding...\n");
	    printf("Wrong format for constant\n");
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(14);
	  }
	if( (LOCCTR-old_locctr)>MC_SIZE )
	  {
	    printf("Constant value too long...\n");
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(50);
	  }
	if( !( (strlen(operand)>=4)&&(operand[1]=='\'')&&(operand[strlen(operand)-1]=='\'') ) )
	  {
	    printf("Format for constant is convoluted at %lX...\n",old_locctr);
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    if(label)
	      free(label);
	    if(operand)
	      free(operand);
	    if(pneumonic)
	      free(pneumonic);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(51);
	  }

      }
    else
      {
	printf("Opcode not found at %lX...\n",LOCCTR);
	fclose(inp_file);
	fclose(int_file);
	free(int_filename);
	free(read_line);
	if(label)
	  free(label);
	if(operand)
	  free(operand);
	if(pneumonic)
	  free(pneumonic);
	free_optab(optab,num_ops);
	free_symtab(symtab);
	exit(15);
      }
      
    if(label)
      free(label);
    if(operand)
      free(operand);
    if(pneumonic)
      free(pneumonic);
    read_line=NULL;
    to_read=0;
    while( (read_len=getline(&read_line,&to_read,inp_file)) != -1) 
      {
	if( (search_space=(char *)malloc(read_len+1)) == NULL )
	  {
	    printf("Out of memory\n");
	    fclose(inp_file);
	    fclose(int_file);
	    free(int_filename);
	    free(read_line);
	    free_optab(optab,num_ops);
	    free_symtab(symtab);
	    exit(10);
	  }
	strcpy(search_space,"");
	sscanf(read_line,"%s",search_space);
	if(((*search_space)=='\0')||((*search_space)==';'))
	  {
	    free(search_space);
	    search_space=NULL;
	    free(read_line);
	    read_line=NULL;
	    continue;
	  }
	free(search_space);
	search_space=NULL;
	break;
      }
    if(read_len == -1)
      {
	printf("Bad assembly coding...\n");
	printf("End of file was reached before END directive\n");
	fclose(int_file);
	fclose(inp_file);
	free(int_filename);
	free_optab(optab,num_ops);
	free_symtab(symtab);
	exit(16);
      }
    label=NULL;
    pneumonic=NULL;
    operand=NULL;
    decode(read_line,read_len,&label,&pneumonic,&operand,int_filename,inp_file,int_file,NULL,optab,num_ops,symtab,LOCCTR,NULL);
    }
  //First Pass finished... Beginning second pass
  if(label)
    free(label);
  if(operand)
    free(operand);
  if(pneumonic)
    free(pneumonic);
  fprintf(int_file,"%lX\t%s",LOCCTR,read_line);
  free(read_line);
  label=NULL;
  operand=NULL;
  pneumonic=NULL;
  read_line=NULL;
  fclose(inp_file);
  out_file=fopen("a.out","w+");
  if( out_file == NULL)
    {
      printf("Failed to open output file...\n");
      fclose(int_file);
      free(int_filename);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(30);
    }
  //Write out the intermediate file and re-open it for second pass
  fclose(int_file);
  int_file=fopen(int_filename,"r");
  if( int_file == NULL)
    {
      printf("Failed to open intermediate file...\n");
      fclose(out_file);
      free(int_filename);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(31);
    }
  
  int_file=fopen(int_filename,"r");
  if( int_file == NULL)
    {
      printf("Failed to open intermediate file...\n");
      fclose(out_file);
      free(int_filename);
      free_optab(optab,num_ops);
      free_symtab(symtab);
      exit(31);
    }
  char *read_raw_line=NULL;
  char string_loc[35];
  while( (read_len=getline(&read_raw_line,&to_read,int_file)) != -1)
    {
      read_raw_line[strlen(read_raw_line)-1]='\0';
      fprintf(out_file,"%s",read_raw_line);    
      read_raw_line[strlen(read_raw_line)]='\n';      
      memset(mc,0,MC_SIZE);
      //We dont have to worry about about newlines spaces etc
      sscanf(read_raw_line,"%s",string_loc);
      read_line=read_raw_line+strlen(string_loc)+1;
      decode(read_line,read_len,&label,&pneumonic,&operand,int_filename,NULL,int_file,out_file,optab,num_ops,symtab,LOCCTR,read_raw_line);      
      if(!label)
	fprintf(out_file,"\t");
      if(!operand)
	fprintf(out_file,"\t");
      char *opcode;
      long int add;
      if( (opcode=search_optab(optab,pneumonic,num_ops)) != NULL )
	{
	  sprintf(mc,"%s",opcode);
	  if(operand)
	    {
	      if( (add=search_symtab(symtab,operand)) > 0 )
		{
		  sprintf(mc+strlen(mc),"%lX",add);
		}
	      else
		{
		  printf("Operand not available in symbol table\n");
		  fclose(int_file);
		  fclose(out_file);
		  free(int_filename);
		  free(read_raw_line);
		  free_optab(optab,num_ops);
		  free_symtab(symtab);
		  exit(35);
		}
	    }
	}
      else if(!strcmp(pneumonic,"BYTE"))
	{
	  convert_const(&operand);
	}
      read_raw_line[strlen(read_raw_line)-1]='\0';
      fprintf(out_file,"\t\t%s\n",mc);    
      if(label)
	free(label);
      if(operand)
	free(operand);
      if(pneumonic)
	free(pneumonic);
      label=pneumonic=operand=NULL;
      
      free(read_raw_line);
      read_raw_line=NULL;
    }
  if(label)
    free(label);
  if(operand)
    free(operand);
  if(pneumonic)
    free(pneumonic);
  fclose(int_file);
  fclose(out_file);
  free(int_filename);
  free_optab(optab,num_ops);
  free_symtab(symtab);
  return 0;
}

