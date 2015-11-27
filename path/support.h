#ifndef SURPORT_H
#define SURPORT_H

#include <deque>
#include <vector>

using namespace std;

struct location{
	int prevRow, prevCol;
	char flag, from;
	bool ifInDeque;
};

void queueMethod(location**, deque <location> *, int&, int&, int&, int&, int, int);



#endif


