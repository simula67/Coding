#include <stdio.h>
#include <stdlib.h>
void print_newline()
{
  printf("\n");
}
void print_ones(int ones)
{
  switch(ones)
    {
    case 1:printf("One ");break;
    case 2:printf("Two ");break;
    case 3:printf("Three ");break;
    case 4:printf("Four ");break;
    case 5:printf("Five ");break;
    case 6:printf("Six ");break;
    case 7:printf("Seven ");break;
    case 8:printf("Eight ");break;
    case 9:printf("Nine ");
    }
}
void print_tens(int tens,int ones)
{
  switch(tens)
    {
    case 0:print_ones(ones);break;
    case 1:
      switch(ones)
	{
	case 0:printf("Ten ");break;
	case 1:printf("Eleven ");break;
	case 2:printf("Twelve ");break;
	case 3:printf("Thirteen ");break;
	case 4:printf("Fourteen ");break;
	case 5:printf("Fifteen ");break;
	case 6:printf("Sixteen ");break;
	case 7:printf("Seventeen ");break;
	case 8:printf("Eighteen ");break;
	case 9:printf("Ninteen ");
	}break;
    case 2:printf("Twenty ");print_ones(ones);break;
    case 3:printf("Thirty ");print_ones(ones);break;
    case 4:printf("Fourty ");print_ones(ones);break;
    case 5:printf("Fifty ");print_ones(ones);break;
    case 6:printf("Sixty ");print_ones(ones);break;
    case 7:printf("Seventy ");print_ones(ones);break;
    case 8:printf("Eighty ");print_ones(ones);break;
    case 9:printf("Ninty ");print_ones(ones);
    }
}     
int main()
{
  atexit(print_newline);
  int num,ones,tens,hunds;
  ones=tens=hunds=0;
  printf("Enter the number : ");
  scanf("%d",&num);
  if(!num)
    {
      printf("Zero ");
      exit(0);
    }
  ones = num%10;
  num/=10;
  if(num<=0)
    {
      print_ones(ones);
      exit(0);
    }
  else
    {
      tens = num%10;
      num /= 10;
      if( num<=0)
	{
	  print_tens(tens,ones);
	  exit(0);
	}
      else
	{
	  hunds = num%10;
	  print_ones(hunds);
	  printf("hundred ");
	  if(tens||ones)
	    printf("and ");
	  print_tens(tens,ones);
	}
    }
}
