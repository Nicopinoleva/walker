#include "sr.h"

#define DEBUG 1

int ip_chk (char *str)
/*  ------  Check if str is valid ip number */
{ int len, num;

  if ((len = strlen (str)) < 1  ||  len > 3  ||
      len != strspn (str, "0123456789")  ||
      (num = atoi (str)) > 255)
    return (0);

  else
    return (num);
}

int my_inet_aton (char *ip_addr, struct in_addr *ip_num)
/*  ------------  Numerize ip_addr into ip_num */
{ int n1, n2, n3, n4;
  char k1 [16], k2 [16], k3 [16];

  ip_num->s_addr = 0;
  if (strlen (ip_addr) > 15)
    return (0);

  n4 = -1;
  sscanf (ip_addr, "%[^.].%[^.].%[^.].%d", k1, k2, k3, &n4);

  if (n4 >= 0  &&  (n1 = ip_chk (k1)) >= 0  &&
      (n2 = ip_chk (k2)) >= 0  &&  (n3 = ip_chk (k3)) >= 0)
    ip_num->s_addr = htonl(n4 + n3 * 256 + n2 * 65536 + n1 * 16777216);

  return (ip_num->s_addr);
}

int Connect (char *ip, int port)
/*  -------  set connection to ip & port returning socket */
{ int sd, socklen;
  struct sockaddr_in sock_in;
  struct in_addr ip_addr;

  if (DEBUG)
    printf ("IP: [%s]  Port: %d\n", ip, port);

  if (my_inet_aton (ip, &ip_addr) == 0)
    return (-1);  // wrong IP
  else if (port < 1)
    return (-2);  // wrong port
  else if ((sd = socket (AF_INET, SOCK_STREAM, 0)) < 0)
    return (-3);  // socket failure
  else
  { socklen = sizeof (struct sockaddr_in);
    memset ((char *)&sock_in, 0, socklen);
    sock_in.sin_family = AF_INET;
    sock_in.sin_port = htons(port);
    sock_in.sin_addr.s_addr = ip_addr.s_addr; // INADDR_ANY

    if (connect (sd, (struct sockaddr *) &sock_in, socklen) < 0)
      return (-errno);  // connect failure
    else
      return (sd);
  }
}

int Send (int sd, char *msg, int len)
/*  ----  send msg to sd returning errno */
{ int lx;
  char str [MAX_MSG+1];

  errno = 0;
  if (len == 0)
    len = strlen (msg);

  if (len < 0)  // send full msg
    send (sd, msg, -len, 0);
  else  // len > 0 => prefix msg with len
  { lx = sprintf (str, "%05d%s", len, msg);
    send (sd, str, lx, 0);
  }

  return (errno);
}

int Recv (int sd, char *msg, int max)
/*  ----  Receive msg from sd returning msglen */
{ int lx, lm,  mx;

  errno = 0;
  mx = max < 0 ? -max : 5;  // max < 0 => receive full msg
  if ((lx = recv (sd, msg, mx, 0)) < 0)
    return (-errno);
  else if (lx == 0)
  { close (sd);
    return (0);
  }
  else if (max < 0)
    return (lx);
  else if (lx != 5)
    return (-9999);
  else if (lx != strspn (msg, "0123456789"))
    return (-9998);
  else
  { mx = atoi (msg);  lm = 0;
    while (lm != mx)
    { if ((lx = recv (sd, msg+lm, mx - lm, 0)) < 0)
        return (-errno);
      else if (lx == 0)
      { close (sd);
        return (0);
      }
      else
        lm += lx;
    }
    return (lm);
  }
}

int SendRecv (int sd, char *send, int len, char *recv, int rmax)
{ int ret;

  if ((ret = Send (sd, send, len)) != 0)
    return (ret);
  else
    return (Recv (sd, recv, rmax));
}

