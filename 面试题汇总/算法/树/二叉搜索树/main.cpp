#include <stdio.h>
#include <stdlib.h>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */
struct node {
	int data;
	node* parent;	//父节点 
	node* rchild;	//右孩子 
	node* lchild;	//左孩子 
};

struct test {
	int bb;
	//char a[3];
	char aa;
	char aaa;
	int b;
	//float c;
}; 

void _insert_node(node* tr,node* p)
{
	if(tr->data >= p->data)	//左子树 
	{
		if(tr->lchild==NULL)
		{
			tr->lchild=p;
			p->parent=tr;
		}
		else
			_insert_node(tr->lchild,p);	
	}
	else
	{
		if(tr->rchild==NULL)
		{
			tr->rchild=p;
			p->parent=tr;
		}
		else
			_insert_node(tr->rchild,p);
	}		
} 

node* insert_node(node* tr,int value)
{
	node* p;
	p=(node*)malloc(sizeof(struct node));
	if(p==NULL)
		printf("insert_node malloc error...");
	else
	{
		p->data=value;
		p->parent=NULL;
		p->lchild=NULL;
		p->rchild=NULL;	
	}
	
	if(tr==NULL)
		tr=p;
	else
		_insert_node(tr,p);
		
	return tr;
}

void delete_node()
{
	//1.根节点 
	//2.叶子节点
	//2.不是叶子节点 
}

//二叉树的前序遍历，根左右  
void pre_list(int arr[],int len,int idx)
{
	if(idx<len)
	{	
		printf("%d ",arr[idx]);

		pre_list(arr,len,idx*2+1);
		pre_list(arr,len,idx*2+2); 
	}
}

//二叉树的中序遍历，左根右
void mid_list(int arr[],int len,int idx)
{
	if(idx<len)
	{
		mid_list(arr,len,2*idx+1);
		printf("%d ",arr[idx]);
		mid_list(arr,len,2*idx+2);
	}	
} 

//二叉树的后序遍历
void lst_list(int arr[],int len,int idx)
{
	if(idx<len)
	{
		lst_list(arr,len,2*idx+1);
		lst_list(arr,len,2*idx+2);
		printf("%d ",arr[idx]);	
	}	
} 

//从小到大输出  
void print_tree(node* tr)
{
	if(tr==NULL)
		return;
	print_tree(tr->lchild);
	printf("%d ",tr->data);
	print_tree(tr->rchild); 
} 

int binary_search(int arr[],int low,int high,int target)
{
	while(low<=high)
	{
		int mid=(low+high)/2;
		if(arr[mid]==target)
			return mid;
		else if(target>arr[mid])
			low=mid+1;
		else if(target<arr[mid])
			high=mid-1;
	}
	
	return -1;
}

int main(int argc, char** argv) {
/*
	node* tr;
	tr=NULL;	 
 
	tr=insert_node(tr,15);
	tr=insert_node(tr,10);
	tr=insert_node(tr,20);
	
	tr=insert_node(tr,8);
	tr=insert_node(tr,12);
	
	tr=insert_node(tr,18);
	tr=insert_node(tr,22);
	
	print_tree(tr);
*/

/*二叉树遍历方法 
	int arr[]={1,2,3,4,5,6,7};
	pre_list(arr,7,0);
	printf("\n");
	mid_list(arr,7,0);
	printf("\n");
	lst_list(arr,7,0);
*/	

/*二分查找 
	int arr[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
	int idx=binary_search(arr,0,15,15); 
	printf("%d",idx);
*/

	printf("%lu",sizeof(struct test));
	return 0;
}
