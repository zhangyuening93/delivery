#include <deque>
#include <iostream>
#include "support.h"

using namespace std;


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




