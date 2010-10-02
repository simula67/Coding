#include<stdio.h>
#include<time.h>
main()
{
time_t now;
now=time(NULL);
printf("\n%lu secs have passed since epoch",(unsigned long)now);
}
