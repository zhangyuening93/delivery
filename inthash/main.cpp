#include "inthash.h"
#include <iostream>

using namespace std;

typedef unsigned int mytype;

int main(){
	mytype result[10];
	mytype num[10]= {0,1,2,3,4,5,6,7,8,9};
	for (int i=0; i<10; i++){
		result[i] = hash_64i(num[i], (1<<8)-1);
		cout << result[i] <<endl;
	}
	for (int i=0; i<10; i++){
		cout << hash_64(result[i], (1<<8)-1)<<endl;
	}
	return 1;
}