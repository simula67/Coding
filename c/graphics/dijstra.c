/*
Author : simula67
*/
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

typedef struct Node {
  int number;
  int parent;
  int cost;
}node;

void bubble_sort(node *queue,int num_elems,int queue_front)
{
  int i,j,temp_number,temp_parent,temp_cost;
  for(i=0;i<num_elems-queue_front;i++) {
    for(j=queue_front;j<num_elems-i-1;j++) {
      if(queue[j].cost > queue[j+1].cost) {
	temp_parent = queue[j].parent;
	temp_number = queue[j].number;
	temp_cost = queue[j].cost;

	queue[j].parent = queue[j+1].parent;
	queue[j].number = queue[j+1].number;
	queue[j].cost = queue[j+1].cost;

	queue[j+1].parent = temp_parent;
	queue[j+1].number = temp_number;
	queue[j+1].cost = temp_cost;
      }
    }
  }
}

int main()
{
  int num_vertices,i,vert1,vert2,weight,queue_front=0,u,v;
  printf("Enter the number of vertices : ");
  scanf("%d",&num_vertices);
  
  node *queue = (node *)malloc(num_vertices * sizeof(node));
  node *res = (node *)malloc(num_vertices * sizeof(node));
  if( (queue == NULL)||(res == NULL) ) {
    fprintf(stderr,"Cannot allocate memmory\n");
    exit(1);
  }
  for(i=0;i<num_vertices;i++) {
    queue[i].number = (i+1);
    queue[i].parent = 0;
    queue[i].cost = INT_MAX;
  }
  
  int **adjmatrix = (int **)malloc(num_vertices *  sizeof(int *));
  if(adjmatrix == NULL ) {
    fprintf(stderr,"Cannot allocate memory\n");
    free(res);
    free(queue);
    exit(1);
  }
  
  for(i=0;i<num_vertices;i++) {
    if( (adjmatrix[i] = (int *)malloc(num_vertices * sizeof(int))) == NULL ) {
      while((i-1)>-1) {
	free(adjmatrix[--i]);
      }
      free(adjmatrix);
      free(res);
      free(queue);
      fprintf(stderr,"Cannot allocate memmory\n");
      exit(1);
    }
  }
  printf("Enter the weights of the edges as vertex1 vertex2 weight : \n");
  printf("eg : 1 2 5\n");
  printf("0 to quit\n");
  while(1) {
    printf("Proceed: ");
    scanf("%d%d%d",&vert1,&vert2,&weight);
    if((vert1==0)||(vert2==0)||(weight==0))
      break;
    adjmatrix[vert1-1][vert2-1] = weight;
    adjmatrix[vert2-1][vert1-1] = weight;
  }
  printf("Enter the starting vertex : ");
  scanf("%d",&vert1);
  queue[(vert1-1)].cost = 0;
  while(queue_front <= (num_vertices-1)) {
    bubble_sort(queue,num_vertices,queue_front);
    res[queue_front] = queue[queue_front];
    for(i=0;i<num_vertices;i++) {
      if(adjmatrix[res[queue_front].number - 1][i] > 0) {//checking the adjacency list of results front node
	for(v=0;queue[v].number!= (i+1);v++);
	for(u=0;queue[u].number!= res[queue_front].number;u++);
	if(queue[v].cost > queue[v].cost + adjmatrix[res[queue_front].number - 1][i]) {
	  queue[v].cost = queue[u].cost + adjmatrix[res[queue_front].number - 1][i];
	  queue[v].parent = queue[u].number;
	}
      }
    }
    queue_front++;
  }
  printf("The result is : \n");
  for(i=0;i<num_vertices;i++) {
    printf("Number : %d\n",res[i].number);
    printf("Cost : %d\n",res[i].cost);
    printf("Parent : %d\n",res[i].parent);
    printf("-----------------------------\n");
  }
  for(i=0;i<num_vertices;i++) {
    free(adjmatrix[i]);
  }
  free(adjmatrix);
  free(res);
  free(queue);
  return 0;
}
