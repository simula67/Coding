#include <QProgressBar>
#include <QApplication>
#include <QTimer>
#include <stdio.h>
int main(int argc,char *argv[])
{
  QApplication *app=new QApplication(argc,argv);
  if(argc!=2) {
    fprintf(stderr,"Error: Too many or too few input to GUI\n");
  }
  else {
    int vol;
    sscanf(argv[1],"%d",&vol);
    QProgressBar *volume=new QProgressBar();
    volume->setValue(vol);
    QTimer::singleShot(1000,app,SLOT(quit()));
    volume->show();
    app->exec();
  }
}
