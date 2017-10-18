#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
void baz();
void bar() { 
baz(); 
}
void foo() { bar(); }
void baz() {
 int *foo = (int*)-1; // make a bad pointer
 printf("%d\n", *foo);       // causes segfault
 FILE* fh fopen("a.txt","w");
 fclose(fh);
}

int main(int argc, char **argv) {
  foo(); // this will call foo, bar, and baz.  baz segfaults.
  exit(0);
}
