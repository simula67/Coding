#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
int main()
{
        signal(SIGCHLD, SIG_IGN);
	extern char **environ;
	printf("Starting artha...\n");
	pid_t artha_fork;
	if( (artha_fork=fork()) < 0 ) {
		fprintf(stderr,"Failed to fork\n");
		exit(1);
	}
	if(artha_fork>0) {
		printf("Successfull fork...\n");
		exit(0);
	}
	char *cmd_line[]={"/usr/bin/artha",NULL};
	execve("/usr/bin/artha",cmd_line,environ);
	fprintf(stderr,"Failed to execute\n");
	return 1;
}
