#include <stdio.h>
#include <stdlib.h>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

struct node {
	int data;
	node* next;
};

struct queue {
	node* begin;
	node* end;
}; 
//Ñ¹ÈëÊý¾Ý 
void push_queue(queue* list,int value)
{
	node* p;
	p=(node*)malloc(sizeof(struct node));
	if(p==NULL)
		printf("push malloc error...");
	else
	{
		p->data=value;
		p->next=NULL;
		
		//queue is empty?
		node* old_end=list->end;
		if(old_end)
			old_end->next=p;
		else
			list->begin=p;
		
		list->end=p;
	}
}

void pop_queue(queue* list)
{
	node* p;
	p=list->begin;
	
	if(p==NULL)		//queue is empty
		printf("queue is empty...");
	else if(p->next==NULL)	//queue havd one node
	{
		list->begin=NULL;
		list->end=NULL;
		free(p);
	}
	else	
	{
		list->begin=p->next;
		free(p);
	}
}

void print_queue(queue* list)
{
	node* p=list->begin;
	while(p!=NULL)
	{
		printf("%d ",p->data);
		p=p->next;
	}
}

int main(int argc, char** argv) {
	
	queue* head;
	head=(queue*)malloc(sizeof(struct queue));
	if(head==NULL)
	{
		printf("main malloc error...");
		return 0;
	}
	else
	{
		head->begin=NULL;
		head->end=NULL;
	}
	int arr[]={1,2,3,4,5};
	for(int i=0;i<5;++i)
	{
		push_queue(head,arr[i]);	
	}
	
	
	pop_queue(head);
	pop_queue(head);
	pop_queue(head);
	//pop_queue(head);
	//pop_queue(head);
	//pop_queue(head);
	print_queue(head);
		
		
	
	return 0;
}
