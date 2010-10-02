#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main(int argc,char *argv[])
{
  if(argc!=2) {
    printf("Usage : %s <object file>\n",argv[0]);
    exit(1);
  }
  FILE *inp_file;
  if( (inp_file=fopen(argv[1],"r")) == NULL ) {
    fprintf(stderr,"reloc: Failed to open input file\n");
    exit(2);
  }
  unsigned long int start_addr; //Starting address Of the program obtained from the Operating System(here read)
  printf("Enter the start address for the program : ");
  scanf("%lu",&start_addr);
 
  unsigned long int curr_addr=start_addr;
  char *read_line=NULL;
  ssize_t read_len;
  size_t to_read=0;
  if( (read_len=getline(&read_line,&to_read,inp_file)) == -1 ) {//Check for file errors
    fprintf(stderr,"reloc: Error... Empty input file\n");
    free(read_line);
    exit(3);
  }
  free(read_line);//free's memory that getline function might have succeded in allocating
  to_read=0;
  read_line=NULL;

  char str_bitmap[4]; //3 char byte for relocation. In integer hex its 12 bits.Least 2 bit is left unused
  str_bitmap[3]='\0';
  char *scan,*end_ptr;
  unsigned int mask;
  long int bitmap;
  char print_buffer[7];
  print_buffer[6]='\0';

  while( (read_len=getline(&read_line,&to_read,inp_file)) != -1 ) {
    if(*read_line=='E') {
      free(read_line);
      read_line=NULL;
      break;
    }
    if(strlen(read_line)<18) {//Maximum Length of the text record.
      fprintf(stderr,"reloc: Screwed up object file input\n");
      free(read_line);
      exit(4);
    }
    strncpy(str_bitmap,read_line+9,3);
    //Copies the relocation bit from read char buffer to another buffer to manipulate it for further calculation
    //For real relocation.
    
    bitmap=strtol(str_bitmap,&end_ptr,16);
    //Got original integer bitmap that can be used for binary operation
    //In integer hex its 12 bits.Least 2 bit is left unused as only maximum 10 words can be mapped
    for(scan=read_line+12,mask=2048;*scan!='\n';scan+=6,mask>>=1,curr_addr+=3) {
      /*
	--scan=read_line+12 -Fetches the First Instruction and further instructions can be further obtained
	                     by the iteration given below 
	--scan+=6       -expanded as scan=scan+6 .Purpose given above
	--mask=2048         -Sets the bitmask to empty setting a '1' in the 11th bit position letting further 
	                     binary and operation possible by just dividing by 2 with iteration given below
        --mask>>=1          -expanded as mask=mask>>1 [equivalent to dividing by 2] purpose explained above
	--curr_addr+=3      -Increment the present loading address by 3 bytes[word size] so that next word is
	                     loaded in the correct memory location
       */
      strncpy(print_buffer,scan,6);
      if(bitmap&mask) {
	sprintf(print_buffer,"%X",start_addr+strtol(print_buffer,&end_ptr,16));
      }
      printf("%X : %s\n",curr_addr,print_buffer);
    }
    free(read_line);
    read_line=NULL; 
  }
return 0;
}
///*--------------------PROGRAM ENDS HERE---------------------------------*///
