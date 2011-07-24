#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "tcp.h"

int send_data(int conn,void *buff,size_t len)
{
  char *scan;
  int sent = 0;
  for(scan=(char *)buff;len!=0;scan=scan+sent,len-=sent) {
    if( (sent = send(conn,scan,len,0)) < 0 ) {
      fprintf(stderr,"Cannot send data over network\n");
      return ERR_SEND;
    }
  }
  return 0;
}
static int recv_line(int sock,void *buff,int max)
{
  int recv_count = 0,ret_stat;
	char *scan=buff;
	while(1) {
		if( (ret_stat = recv(sock,scan,1,0)) > 0 ) {
			recv_count++;
			  if(recv_count == max)
			    return recv_count;
			  if( scan[0] == '\r' ) {
			    /* 
			       Possible end of string. Get the next character and check if its '\n'
			    */
			    scan++;
			    if( (ret_stat = recv(sock,scan,1,0)) > 0 ) {
			      recv_count++;
			      if(recv_count == max)
				return recv_count;
			      if( scan[0] == '\n' )
				return recv_count;
			    }
			    else
			      return ret_stat;			  
			  }
			  scan++;
		}
		else
		  return ret_stat;
	}
}
char *recv_data(int sock)
{
  int count_recv,buff_len=INIT_BUFF_LEN;
  char temp_recv[INCR_BUFF];
  char *buff,*temp,*end=NULL;
  if( sock <= 0 ) {
    fprintf(stderr,"Incorrect socket passed\n");
    return NULL;
  }
  if( (buff = malloc( buff_len * sizeof(char) )) == NULL ) {
    fprintf(stderr,"Out of memmory\n");
    return NULL;
  }
  if( (count_recv = (recv_line(sock,buff,(INIT_BUFF_LEN-1)))) <= 0 ) {
    if(count_recv = 0) {
      fprintf(stderr,"Connection to server lost\n");
      free(buff);
      return NULL;
    }
    if(count_recv < 0) {
      fprintf(stderr,"Error in connection\n");
      free(buff);
      return NULL;
    }
  }
  if( (end = strstr(buff,"\r\n")) != NULL ) {
    end[2]='\0';
    return buff;
  }
  while(end == NULL) {
    if( (temp = malloc( buff_len + INCR_BUFF )) == NULL ) {
      fprintf(stderr,"Out of memmory\n");
      free(buff);
      return NULL;
    }
    memset(temp,0,buff_len+INCR_BUFF);
    memcpy(temp,buff,((buff_len-1) * sizeof(char)));
    free(buff);
    buff=temp;
    if( (count_recv = (recv_line(sock,temp_recv,INCR_BUFF))) <= 0 ) {
      if(count_recv = 0) {
	fprintf(stderr,"Connection to server lost\n");
	free(buff);
	return NULL;
      }
      if(count_recv < 0) {
	fprintf(stderr,"Error in connection\n");
	free(buff);
	return NULL;
      }
    }
    memcpy(buff + buff_len - 1,temp_recv,count_recv * sizeof(char));
    buff_len += INCR_BUFF;
    end=strstr(buff,"\r\n");
  }
  end[2]='\0';
  return buff;
}

int connect_to_server(char *host,char *port)
{
  int conn;
  struct addrinfo hints, *res,*scan;
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_INET;
  hints.ai_socktype = SOCK_STREAM;
  
  if( getaddrinfo(host, port, &hints, &res) != 0 ) {
    fprintf(stderr,"Failed to lookup name : %s\n",host);
    return ERR_LOOKUP;
  }
  
  for(scan=res;scan!=NULL;scan=scan->ai_next) {
    if( (conn = socket(scan->ai_family, scan->ai_socktype, scan->ai_protocol)) > 0 ) {
      if( (connect(conn, scan->ai_addr, scan->ai_addrlen)) == 0 ) {
    	  freeaddrinfo(res);
    	  return conn;
      }
    }
  }
  freeaddrinfo(res);
  fprintf(stderr,"Failed to connect to server at %s:%s\n",host,port);
  return ERR_CONN;
}
int setup_server(char *port,int backlog) {
  int lis_sock;
  struct addrinfo hints,*scan,*res;
  memset(&hints, 0, sizeof(hints));
  hints.ai_family = AF_INET;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;
  if( getaddrinfo(NULL, port, &hints, &res) != 0 ) {
    fprintf(stderr,"Failed to lookup the local address");
    return ERR_LOOKUP;
  }
  
  for(scan=res;scan!=NULL;scan=scan->ai_next) {
    if( (lis_sock = socket(scan->ai_family, scan->ai_socktype, scan->ai_protocol)) < 0  ) {
      fprintf(stderr,"Failed to setup server\n");
      return ERR_SERV;
    }
    if( bind(lis_sock,scan->ai_addr,scan->ai_addrlen) != 0 ) {
      fprintf(stderr,"Failed to setup server\n");
      return ERR_SERV;
    }
    if( listen(lis_sock,backlog) != 0 ) {
      fprintf(stderr,"Failed to setup server\n");
      return ERR_SERV;
    }
    return lis_sock;
  }
  fprintf(stderr,"No suitable address\n");
  return ERR_SERV;
}
