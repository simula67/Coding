#include <QPushButton>
#include <unistd.h>
#include <QApplication>
class Shutdown : public QObject {
	Q_OBJECT
	private slots:
	void do_shutdown();	
};
