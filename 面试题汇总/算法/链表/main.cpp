#include<stdio.h>
#include<stdlib.h>
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

struct node{
	int data;
	node* next;
}; 

//��ӡ�������� 
void print_list(node* list)
{
	if(list->next!=NULL)
	{
		node* head=list->next;
		while(head!=NULL)
		{
			printf("%d ",head->data);
			head=head->next;	
		}		
	}	
}

//�����������,ͷ�巨 
void insert_node(node* list,int data)
{
	node* p;
	p=(node*)malloc(sizeof(struct node));
	if(p==NULL)
		printf("insert_node malloc error...");
	else
	{
		p->data=data;
		p->next=list->next;
		list->next=p;	
	} 	
} 

//ɾ���ڵ�
void delete_node(node* list,int data)
{
	node* p=list->next;		//������Ҫɾ���Ľڵ� 
	node* prenode=list;		//��¼ɾ���ڵ��ǰһ���ڵ� 
	while(p!=NULL)
	{
		if(p->data==data)
		{
			prenode->next=p->next;
			free(p);	
			break;
		}	
		prenode=p;
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
		insert_node(head,arr[i]);
	}
	
	delete_node(head,1);
	
	print_list(head);
	
		
	return 0;
}
