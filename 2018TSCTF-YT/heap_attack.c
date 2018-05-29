#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include <unistd.h>

char *s[12];

void prepare()
{
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
}
void echo()
{
    system("echo 'welcome to TSCTF!'");
}
void inputContent(char *buf,int len)
{
    printf("Input content:");
    read(0,buf,len-1);
    buf[len-1]=0;
}
void newBlock()
{
    int size,i;
    char *block;

    printf("Input size:");
    scanf("%d",&size);
    //getchar();
    block = malloc(size);
    inputContent(block,size);

    for(i=0;i<9 && s[i];++i);
    if (i==10)
	exit(0); 
    s[i]=block;
    printf("Successfully add.\n");
}
void deleteBlock()
{
    int index;
    printf("Input index:");
    scanf("%d",&index);
    //getchar();
    
    if(index>=0 && index<=9)
    {
	free(s[index]);
        printf("Successfully delete.\n");
    }
}
void editBlock()
{
    int index,len;
    printf("Input index:");
    scanf("%d",&index);
    getchar();

    if(index>=0 && index<=9)
    {
	len = strlen(s[index]);
        inputContent(s[index],len+1);
        printf("Successfully edit.\n");
    }
}
int main()
{
    int num;
    prepare();
    echo();
    while(1)
    {
        printf("===============menu==============\n");
	printf("1.Add\n2.Delete\n3.Edit\n");
        printf("Input ur choice:");
        scanf("%d",&num);
        //getchar();
	switch(num)
	{
	    case 1:
		newBlock();
		break;
	    case 2:
		deleteBlock();
		break;
	    case 3:
		editBlock();
		break;
	}
    }
}
