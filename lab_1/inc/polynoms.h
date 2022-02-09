#ifndef MY_POLYNOM
#define MY_POLYNOM

#include "struct.h"
int get_newton_polynomial(newton_polynomial *newton, const table_t *func_table);
int get_hermit_polynomial(hermit_polynomial *hermit, const table_t *func_table);
int compare(table_t *table);

#endif
