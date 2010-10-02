/*
Linux implementation of nslookup. This implementation can lookup many IP addresses in one go.
Coded by : simula67
*/
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<arpa/inet.h>
int main(int argc,char *argv[])
{
  struct addrinfo hints;
  struct addrinfo *res;
  struct addrinfo *scan;
  void *to_print;
  char ans[25];
  memset(&hints,0,sizeof(hints));
  hints.ai_family=AF_UNSPEC;
  hints.ai_socktype=SOCK_STREAM;
  if(argc<2)
    {
      printf("Usage : %s <names to lookup>\n",argv[0]);
      exit(1);
    }
  int i;
  for(i=1;i<argc;i++)
    {
      if( getaddrinfo(argv[i],NULL,&hints,&res)!= 0 )
	{
	  printf("Failed to lookup name : \"%s\"\n",argv[i]);
	  continue;
	}
      for(scan=res;scan!=NULL;scan=scan->ai_next)
	{
	  to_print=scan->ai_addr;
	  if(scan->ai_family==AF_INET)
	    {
	      if( inet_ntop(AF_INET,&(((struct sockaddr_in *)to_print)->sin_addr),ans,sizeof(ans))==NULL )
		{
		  printf("Converting to presentation form failed(IPv4) for %s\n",argv[i]);
		  continue;
		}
		printf("%s (IPv4) : %s\n",argv[i],ans);
	    }
	  else if(scan->ai_family==AF_INET6)
	    {
	      if( inet_ntop(AF_INET6,&(((struct sockaddr_in6 *)to_print)->sin6_addr),ans,sizeof(ans))==NULL )
		{
		  printf("Converting to presentation form failed for(IPv6) %s\n",argv[i]);
		  continue;
		}
		printf("%s (IPv6) : %s\n",argv[i],ans);
	    }
	  else
	    {
	      printf("Address family not recognized\n");
	    }
	}
      freeaddrinfo(res);
    }
  return 0;
}
