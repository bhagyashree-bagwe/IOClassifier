#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include "t2.cpp"
void baz();
void bar() { 
baz(); 
}
void foo(int a,int b) { 
a=a+1;
bar(); 
}
void baz() {
 int *foo = (int*)-1; // make a bad pointer
 FILE* fh=fopen("a.txt","w");
 fclose(fh);
}
class A{
public:
void hello(){
}
};
int main(int argc, char **argv) {
  int c=11;
  int a=12+10;
  int b;
  b=12;
//  for(int i=0;i<10;i++){
  b+=1;
//  }
//  while(true)
//  {
a+=1;
//  }
//  for(int i=0;i<10;i++) 
b+=1;
 foo(a,b); // this will call foo, bar, and baz.  baz segfaults.
b+=1;
foo(a,b);
  A object=A();
  object.hello();
  exit(0);
}

