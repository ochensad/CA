#ifndef MY_TABLE
#define MY_TABLE

#include "struct.h"

int allocate_table(table_t *table);
void free_table(double **table, int n);
int read_file(char *filename, table_arr_t *table);
void print_func_table(table_arr_t* table);
void sort_table(table_t *table);
#endif