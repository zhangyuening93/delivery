#include <python2.7/Python.h>
#include <iostream>
#include <cstdlib>
#include <string>
#include <sstream>
#include <deque>
#include <vector>
#include <getopt.h>

using namespace std;

struct location{
	int prevRow, prevCol;
	char flag, from;
	bool ifInDeque;
};


int Dot_Map[20][10] = {{1, 1, 1, 1, 0},
                       {0, 0, 0, 1, 0},
                       {0, 0, 1, 1, 1},
                       {0, 0, 0, 1, 0},
             	       {0, 0, 1, 1, 1}};

void queueMethod(location** Map, deque<location> *RouteHelper,  
				 int& destination_row, int& destination_col, 
				 int& start_row, int& start_col, 
				 int room_row, int room_col)
{
	while(1){
		int row = 0, col = 0;
		if(RouteHelper->empty()){
			break;
		}

		location temp;
		temp = RouteHelper->front();
		RouteHelper->pop_front();

		if(temp.from == 'n'){
			row = temp.prevRow - 1;
			col = temp.prevCol;
		}
		else if(temp.from == 's'){
			row = temp.prevRow + 1;
			col = temp.prevCol;
		}
		else if(temp.from == 'e'){
			row = temp.prevRow;
			col = temp.prevCol + 1;
		}
		else if(temp.from == 'w'){
			row = temp.prevRow;
			col = temp.prevCol - 1;
		}
		else if(temp.from == '\0'){
			row = start_row;
			col = start_col;
		}

		if(row-1>=0){
			if(Map[row-1][col].flag != '#' &&
			   Map[row-1][col].ifInDeque == false){

				Map[row-1][col].prevCol = col;
				Map[row-1][col].prevRow = row;
				Map[row-1][col].ifInDeque = true;
				Map[row-1][col].from = 'n';
				RouteHelper->push_back(Map[row-1][col]);

				if(Map[row-1][col].flag == 'D'){
					destination_row = row - 1;
					destination_col = col;
					break;
				}
			}
		}

		if(col-1>=0){
			if(Map[row][col-1].flag != '#' &&
			   Map[row][col-1].ifInDeque == false){

				Map[row][col-1].prevCol = col;
				Map[row][col-1].prevRow = row;
				Map[row][col-1].ifInDeque = true;
				Map[row][col-1].from = 'w';
				RouteHelper->push_back(Map[row][col-1]);

				if(Map[row][col-1].flag == 'D'){
					destination_row = row;
					destination_col = col-1;
					break;
				}
			}
		}

		if(row+1 < room_row){
			if(Map[row+1][col].flag != '#' &&
			   Map[row+1][col].ifInDeque == false){

				Map[row+1][col].prevCol = col;
				Map[row+1][col].prevRow = row;
				Map[row+1][col].ifInDeque = true;
				Map[row+1][col].from = 's';
				RouteHelper->push_back(Map[row+1][col]);

				if(Map[row+1][col].flag == 'D'){
					destination_row = row+1;
					destination_col = col;
					break;
				}
			}
		}

		if(col+1 < room_col){
			if(Map[row][col+1].flag != '#' &&
			   Map[row][col+1].ifInDeque == false){

				Map[row][col+1].prevCol = col;
				Map[row][col+1].prevRow = row;
				Map[row][col+1].ifInDeque = true;
				Map[row][col+1].from = 'e';
				RouteHelper->push_back(Map[row][col+1]);

				if(Map[row][col+1].flag == 'D'){
					destination_row = row;
					destination_col = col+1;
					break;
				}
			}
		}
	}
}


string GetCommand(int start_row, int start_col, 
						int destination_row, int destination_col){
	vector<char> reverse;
	deque <location> RouteHelper;

    location** Map = new location* [20];
	for (int i=0; i<20; i++){
		Map[i] = new location[10];
	}	

	int i = 0;
	int j = 0;
	for(i=0; i<20; i++){
		for(j=0; j<10; j++){
			Map[i][j].prevCol = -1;
			Map[i][j].prevRow = -1;
			Map[i][j].from = '\0';
			Map[i][j].ifInDeque = false;
			if(Dot_Map[i][j] == 1)
				Map[i][j].flag = '.';
			else
				Map[i][j].flag = '#';

			if(i == destination_row && j == destination_col)
				Map[i][j].flag = 'D';			
		}
	}

	Map[start_row][start_col].ifInDeque = true;
	RouteHelper.push_back(Map[start_row][start_col]);
	queueMethod(Map, &RouteHelper, destination_row, destination_col, start_row, start_col, 20, 10);
	deque<location> Route;
	Route.push_back(Map[destination_row][destination_col]);

	while(1){
		location temp = Route.back();
		if(temp.prevCol == -1)
			break;
		reverse.push_back(temp.from);
		Route.push_back(Map[temp.prevRow][temp.prevCol]);
	}
	string result;

	for(int i = (int)reverse.size()-1; i>=0; i--){
		result.append(1,reverse[i]);
	}

	return result;
}



static PyObject* exmodError;

static PyObject* exmod_find_route(PyObject* self, PyObject *args){
	int start_row;
	int start_col;
	int destination_row;
	int destination_col;
	string s;

	if(!PyArg_ParseTuple(args, "iiii", &start_row, &start_col, 
									   &destination_row, &destination_col))
		return NULL;

	s = GetCommand(start_row, start_col, destination_row, destination_col);


	return Py_BuildValue("s", s.c_str());
}


static PyMethodDef exmod_methods[] ={
	{"find_route", exmod_find_route, METH_VARARGS, "Find the route based on user's input"},
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initexmod(void){
	PyObject* m;
	m = Py_InitModule("exmod", exmod_methods);
	if(m == NULL) return;
	
	exmodError = PyErr_NewException("exmod.error", NULL, NULL);
	Py_INCREF(exmodError);

	PyModule_AddObject(m, "error", exmodError);
}




// int main(int argc, char* argv[]){
// 	// int room_col, room_row; 
// 	// int destination_row = -1, destination_col = -1;
// 	// int start_row, start_col;

// 	// string read;

// 	// cin >> room_row;
// 	// cin >> room_col;

//  	//Build each position.
// 	// location** Map = new location* [room_row];
// 	// for (int i=0; i<room_row; i++){
// 	// 	Map[i] = new location[room_col];
// 	// }

// 	// //Initialize the castle.
// 	// for(int i=0; i<room_row; i++){
// 	// 	for(int j=0; j<room_col; j++){
// 	// 		Map[i][j].prevRow = -1;
// 	// 		Map[i][j].prevCol = -1;
// 	// 		Map[i][j].flag = '.';
// 	// 		Map[i][j].ifInDeque = false;
// 	// 		Map[i][j].from = '\0';
// 	// 	}
// 	// }

// 	//Read the map.
// 	// getline(cin,read);
// 	// getline(cin,read);
// 	// for(int i=0; i<room_row; i++){
// 	// 	istringstream iStream;
// 	// 	iStream.str(read);
// 	// 	for(int j=0; j<room_col; j++){
// 	// 		iStream >> Map[i][j].flag;

// 	// 		if(Map[i][j].flag == 'S'){
// 	// 			start_row = i;
// 	// 			start_col = j;
// 	// 			Map[i][j].ifInDeque = true;
// 	// 		}
// 	// 	}
// 	// 	getline(cin,read);
// 	// }

// 	string result;
	
// 	result = GetCommand(13, 9, 19, 0);
// 	cout << result;
// 	cout << endl;
// 	return 0;

// }
