#ifndef MY_STRUCT
#define MY_STRUCT

typedef struct
{
    double **table;
    int rows;
    int columns;
} table_t;

typedef struct
{
    table_t diff_table;
    double *x_values;
    int polynom_exp;
    double value_to_find;
    double y_value;
}newton_polynomial;

#endif