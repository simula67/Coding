#include <stdlib.h>
#include <unistd.h>
#include <vga.h>
#include <stdio.h>
void set_mode()
{
  vga_setmode(TEXT);
}
int main(void)
{
  atexit(set_mode);
  int color = 9;
  //  int x = 10;
  //  int y = 10;
  //  unsigned int seconds = 5;
 
  /* detect the chipset and give up supervisor rights */
  /*
  if (vga_init() < 0) {
    fprintf(stderr,"Cannot init");
    return EXIT_FAILURE;
  } 
  */
  int mode = vga_getdefaultmode();
  if (vga_setmode(mode) < 0 ) {
    fprintf(stderr,"Cannot set mode");
    exit(1);
  }
  vga_setcolor(color);
  vga_drawline(0,0,50,50);
 
  //  sleep(seconds);
 
  scanf("%d",&color);
  return EXIT_SUCCESS;
}
