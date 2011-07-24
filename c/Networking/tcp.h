#ifndef _TCP_H
#define _TCP_H

#define ERR_LOOKUP -1
#define ERR_CONN -2
#define ERR_SEND -3
#define ERR_SERV -4
#define INIT_BUFF_LEN 65
#define INCR_BUFF 10


extern int send_data(int conn,void *buff,size_t len);
extern char *recv_data(int sock);
extern int connect_to_server(char *host,char *port);
extern int setup_server(char *port,int backlog);
#endif
