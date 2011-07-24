
#include "shutdown.h"
void Shutdown::do_shutdown()
{
	char *env[] = { NULL };
    char *comm[] = { "-hP" , "now" , NULL };
    execve("/sbin/shutdown",comm,env);
}
int main(int argc,char *argv[])
{
	QApplication *app=new QApplication(argc,argv);
	QPushButton *shutdown = new QPushButton("Shutdown");
	shutdown->show();
	Shutdown dummy;
	QObject::connect(shutdown,SIGNAL(clicked()),&dummy,SLOT(do_shutdown()));
	
	return app->exec();
}
