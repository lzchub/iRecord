#include <stdio.h>
#include <stdlib.h>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

struct node {
	int data;
	node* next;
};

//Ñ¹ÈçÊý¾Ý 
void push(node* list,int value)
{
	node* p;
	p=(node*)malloc(sizeof(struct node));
	if(p==NULL)
		printf("push malloc error...");
	else
	{
		p->data=value;
		p->next=list->next;
		list->next=p;
	}
}

void pop(node* list)
{
	if(list->next!=NULL)
	{
		node* p=list->next;
		list->next=p->next;
		free(p);
	} 
	else
		printf("list is empty...");
}

void print_list(node* list)
{
	node* p=list->next;
	while(p!=NULL)
	{
		printf("%d ",p->data);
		p=p->next;
	}
}

int main(int argc, char** argv) {
	
	node* head;
	head=(node*)malloc(sizeof(struct node));
	if(head==NULL)
	{
		printf("main malloc error...");
		return 0;
	}
	else
		head->next=NULL;
	
	int arr[]={1,2,3,4,5};
	for(int i=0;i<5;++i)
	{
		push(head,arr[i]);	
	}
	
	pop(head);
	pop(head);
	print_list(head);
		
		
	
	return 0;
}
