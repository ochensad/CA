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
    table_t *table;
    int size;
} table_arr_t;

typedef struct
{
    table_t diff_table;
    double *x_values;
    int polynom_exp;
    double value_to_find;
    double y_value;
}newton_polynomial;

typedef struct
{
    int n_x;
    int n_y;
    int n_z;
}n_exp;

typedef struct
{
    double x_to_find;
    double y_to_find;
    double z_to_find;
    double* x_values;
    double* y_values;
    double* z_values;
    n_exp exps;
} data_t;



#endif