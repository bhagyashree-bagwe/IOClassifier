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
void foo() { 
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
}
int main(int argc, char **argv) {
  foo(); // this will call foo, bar, and baz.  baz segfaults.
  A object=A();
  object.hello();
  exit(0);
}

