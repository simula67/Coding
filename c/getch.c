#include <stdio.h>
#include <termios.h>
#include <unistd.h>

int getch() 
{
  struct termios oldt, newt;
  int ch;
  tcgetattr( STDIN_FILENO, &oldt );
  newt = oldt;
  newt.c_lflag &= ~( ICANON | ECHO );
  tcsetattr( STDIN_FILENO, TCSANOW, &newt );
  ch = getchar();
  tcsetattr( STDIN_FILENO, TCSANOW, &oldt );
  return ch;
}


//Example use
int main()
{
  char ch;
  printf("Enter a character : ");
  ch=getch();
  printf("\nThe entered character is : %c\n",ch);
  return 0;
}
