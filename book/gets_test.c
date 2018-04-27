#include<stdio.h>
int main(){
   char a,*s;
   s = malloc(10);
   do 
     a = getchar();
   while(a!=10 && a!=-1);
   gets(s);
   puts(s);
}
