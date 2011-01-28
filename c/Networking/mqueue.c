#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <mqueue.h>
#include <assert.h>

#define MAXLEN 10000

int
main(int argc,char *argv[])
{
  assert( argc==2 );
  char send_message[MAXLEN];
  char rec_message[MAXLEN];
  pid_t cpid;
  mqd_t myqueue;
  ssize_t received;
  unsigned int priority;
  strcpy(send_message,"");
  strcpy(rec_message,"");
   /*
  struct timespec abs_timeout;
  memset(&abs_timeout,sizeof(struct timespec),0);
  abs_timeout.tv_sec = 5;
  */
  if( (myqueue = mq_open(argv[1], O_RDWR | O_CREAT)) == ( (mqd_t) - 1 ) ) {
    fprintf(stderr,"Cant open message queue\n");
    exit(1);
  }  
  cpid = fork();
  if( cpid < 0 ) {
    fprintf(stderr,"Failed to fork\n");
    exit(1);
  }
  if( cpid == 0 ) {
    /* Child */
    while( strcmp(rec_message,"STOP") ) {
      if( (received = mq_receive(myqueue,rec_message,MAXLEN,&priority)) < 0 ) {
	fprintf(stderr,"Cannot read from message queue\n");
	exit(1);
      }
      printf("Child received : %s\n",rec_message);
    }
    exit(0);
  }
  /* Parent */
  while(1) {
    printf("Enter string to put in message queue (MAX 50 CHARACTERS) : ");
    fgets(send_message,MAXLEN,stdin);
    send_message[ strlen(send_message) - 1 ] = '\0';
    if( mq_send(myqueue,send_message,strlen(send_message),0) != 0 ) {
      fprintf(stderr,"Failed to send message\n");
      exit(1);
    }
    if(!strcmp(send_message,"STOP"))
      break;
  }
  if( mq_close(myqueue)!= 0 ) {
    fprintf(stderr,"Cannot close message queue\n");
    exit(1);
  }
  if( mq_unlink(argv[1]) != 0 ) {
    fprintf(stderr,"Cannot unlink message queue\n");
    exit(1);
  }
  wait(NULL);
  return 0;
}
