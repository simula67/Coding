#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
const int prime1=17;
const int prime2=19;
unsigned int modpow(int,int,int);
int gcd(int num1,int num2)
{
  return((num2==0)?num1:gcd(num2,num1%num2));
}

int gen_publickey(int totient);
int gen_privatekey(int totient,int publickey);
main()
{
  int moduluo=prime1*prime2;
  int totient=(prime1-1)*(prime2-1);
  printf("\nTotient is : %d",totient);
  char message[]="Jogy Antony";
  char retrieved[25];
  int cypher[50];
  int i;
  int public_key[2];
  public_key[0]=gen_publickey(totient);
  printf("\nPublic Key is : %d ",public_key[0]);
  public_key[1]=moduluo;
  unsigned long int power;
  for(i=0;i<strlen(message);i++)
    {
      cypher[i]=modpow(message[i],public_key[0],moduluo);;
    }
  int private_key[2];
  private_key[0]=gen_privatekey(totient,public_key[0]);
  private_key[1]=moduluo;
  printf("\nPrivate Key is : %d",private_key[0]);
  for(i=0;i<strlen(message);i++)
    {
      
      retrieved[i]=(char)modpow(cypher[i],private_key[0],moduluo);  

    }
  printf("\nDecrypted message is : ");
  retrieved[strlen(message)]='\0';
  puts(retrieved);
  printf("\n");
}
int gen_publickey(int totient)
{  
  int i;
  for(i=2;i<totient;i++)
    {
      if(gcd(totient,i)==1)
	return i;
    }
  printf("\nEncryption failed...\n");
  exit(0);
}
int gen_privatekey(int totient,int publickey)
{
  unsigned int i=totient+1;
  unsigned int num;
  do
    {
      num=(publickey*i)-1;
      if(!(num%totient))
	return i;
      i++;
    }while(i>totient);
  printf("\nDecryption failed..\n");
}
unsigned int modpow(int base,int exponent,int modulus) 
{
 
  unsigned long int result = 1;
 
  while (exponent > 0) 
    {
      if ((exponent & 1) == 1) 
	{
      // multiply in this bit's contribution while using modulus to keep result small
	  result = (result * base) % modulus;
	}
    // move to the next bit of the exponent, square (and mod) the base accordingly
      exponent >>= 1;
      base = (base * base) % modulus;
    }
 
  return result;
}
