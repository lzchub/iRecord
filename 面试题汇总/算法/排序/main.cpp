
#include <iostream>
using namespace std;
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

//1.√∞≈›≈≈–Ú 
void bubble_sort(int arr[],int len)
{
	for(int i=0;i<len-1;i++) 
	{
		for(int j=0;j<len-1-i;j++)
		{
			int temp;
			if(arr[j]>arr[j+1])
			{
				temp=arr[j];
				arr[j]=arr[j+1];
				arr[j+1]=temp;
			}
		}
	}
}
  
//2.—°‘Ò≈≈–Ú
void select_sort(int arr[],int len)
{
	for(int i=0;i<len-1;i++)
	{
		for(int j=i+1;j<len;j++)
		{
			int temp;
			if(arr[i]>arr[j])
			{
				temp=arr[i];
				arr[i]=arr[j];
				arr[j]=temp;
			}
		}
	}	
} 

//3.≤Â»Î≈≈–Ú
void insert_sort(int arr[],int len)
{
	for(int i=1;i<len;i++)
	{
		for(int j=i;j>0;j--)
		{
			if(arr[j]<arr[j-1])
			{
				int temp=arr[j];
				arr[j]=arr[j-1];
				arr[j-1]=temp;
			}
			else
				break;
		}
	}
} 

//4.œ£∂˚≈≈–Ú 
void shell_sort(int arr[],int len)
{
	int step=len>>1;	//≤Ω≥§
	
	while(step!=0)
	{
		for(int i=step;i<len;i++)
		{
			int j=i-step;
			int temp=arr[i]; 
			
			while(j>=0 && arr[j]>temp)
			{
				arr[j+step]=arr[j];
				j-=step;
			}
			arr[j+step]=temp;	
		}
		step=step>>1;
	} 
}

//5.øÏÀŸ≈≈–Ú
void quick_sort(int arr[],int begin,int end)
{
	if(begin>=end)
		return;
	int key=arr[begin];
	int low=begin;
	int high=end;
	
	while(low < high)
	{
		while(low<high && key<=arr[high])
		{
			high--;
		}
		arr[low]=arr[high];
	
		while(low<high && key>=arr[low])
		{
			low++;
		}
		arr[high]=arr[low];
	}
	arr[low]=key;
	
	quick_sort(arr,begin,low-1);
	quick_sort(arr,low+1,end);
}

//∂—≈≈–Ú

//πÈ≤¢≈≈–Ú 



int main(int argc, char** argv) {
	
	 
	int arr[]={1,4,2,6,8,3,9,11,3,2};
	//bubble_sort(arr,6);
	//select_sort(arr,6);
	//insert_sort(arr,6);
	//shell_sort(arr,10);
	//quick_sort(arr,0,9);
	for(int i=0;i<10;i++)
	{	//printf("%d ",arr[i]);
		cout << arr[i] <<" ";
	}
	return 0;
}
