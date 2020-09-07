#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAX_MSG  1000

int ip_chk (char *str);
/*  ------  Check if str is valid ip number */

int my_inet_aton (char *ip_addr, struct in_addr *ip_num);
/*  ------------  Numerize ip_addr into ip_num */

int Connect (char *ip, int port);
/*  -------  set connection to ip & port returning socket */

int Send (int sd, char *msg, int len);
/*  ----  send msg to sd returning errno */

int Recv (int sd, char *msg, int max);
/*  ----  Receive msg from sd returning msglen */

int SendRecv (int sd, char *send, int len, char *recv, int rmax);
/*  --------  Send & receive msg */
