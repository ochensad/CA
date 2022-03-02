#include "polynoms.h"
#include "errors.h"
#include "table.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define EPS 10e-10

int find_index_in_table(double value, const table_t *func_table)
{
    int index = 0;
    for (int i = 0; i < func_table->rows; i++)
    {
        if (fabs(func_table->table[i][0] - value) < EPS)
        {
            return -1;
        }
        if (func_table->table[i][0] < value)
        {
            index = i;
        }
    }
    return index;
}

int find_value_to_newton_table(newton_polynomial *newton,const table_t *func_table, int i_find)
{
    int get_left;
    int get_right;
    if ((newton->polynom_exp + 1) / 2 > (i_find + 1))
    {
        get_left = i_find + 1;
        get_right = (newton->polynom_exp + 1) - get_left;
    }
    else if ((newton->polynom_exp + 1) / 2 > (func_table->rows - i_find))
    {
        get_right = func_table->rows - i_find - 1;
        get_left = (newton->polynom_exp + 1) - get_right;
    }
    else
    {
        get_left = (newton->polynom_exp + 1)/2;
        get_right = (newton->polynom_exp + 1) - get_left;
    }

    newton->diff_table.rows = (newton->polynom_exp + 1);
    newton->diff_table.columns = (newton->polynom_exp + 1);
    int error_code = allocate_table(&newton->diff_table);
    if (error_code)
    {
        printf("Ошибка выделения памяти\n");
        return error_code;
    }

    newton->x_values = calloc(newton->polynom_exp + 1, sizeof(double));
    if (newton->x_values == NULL)
    {
        printf("Ошибка выделения памяти\n");
        return ERROR_MEMORY;
    }

    int j = 0;
    for (int i = 0; i < func_table->rows; i++)
    {
        if ((i >= i_find - get_left + 1) && (i <= i_find + get_right))
        {
            newton->diff_table.table[j][0] = func_table->table[i][1];
            newton->x_values[j] = func_table->table[i][0];
            j++;
        }
    }
    return OK;
}

void fill_newton_table(newton_polynomial *newton)
{
    double x;
    for (int j = 0; j < newton->polynom_exp; j++)
    {
        for (int i = 0; i < newton->polynom_exp - j; i++)
        {
            x = (newton->diff_table.table[i][j] - newton->diff_table.table[i + 1][j]) / (newton->x_values[i] - newton->x_values[i + 1 + j]);
            newton->diff_table.table[i][j + 1] = x;
        }
    }
}

void count_newton_polynomial(newton_polynomial *newton)
{
    double value = 0;
    double buf = 1;
    double x_value = 0;
    for(int i = 0; i <= newton->polynom_exp; i++)
    {
        x_value = newton->diff_table.table[0][i];
        for (int j = 0; j < i; j++)
        {
            buf *= (newton->value_to_find - newton->x_values[j]);
        }
        value += (x_value * buf);
        buf = 1;
        x_value = 0;
    }
    newton->y_value = value;
}

void print_table(newton_polynomial *newton)
{
    printf("Таблица разностей\n\n");
    for(int i = 0; i <= newton->polynom_exp; i++)
    {
        for(int j = 0; j <= newton->polynom_exp - i; j++)
            printf(" %lf", newton->diff_table.table[i][j]);
        printf("\n");
    }
}

int get_newton_polynomial(newton_polynomial *newton, const table_t *func_table)
{
    int i_find = find_index_in_table(newton->value_to_find, func_table);

    int error_code = find_value_to_newton_table(newton, func_table, i_find);
    if (error_code)
        return error_code;
    
    fill_newton_table(newton);
    print_table(newton);
    count_newton_polynomial(newton);
    printf("Значение y(x): %lf\n", newton->y_value);
    return OK;
}

void check_min()

int get_points(data_t* data, table_arr_t table)
{
    data->x_values = calloc(data->exps.n_x + 1, sizeof(double));
    data->y_values = calloc(data->exps.n_y + 1, sizeof(double));
    data->z_values = calloc(data->exps.n_z + 1, sizeof(double));
    
    double ab = 1000000.0;
    double min = 1000000.0;
    for(int i = 0; i < table.size; i++)
    {
        for(int j = 1; j < table.table[i].rows; j++)
        {
            for(int k = 1; k < table.table[i].columns; k++)
            {
                ab = sqrt(pow(table.table[i].table[0][k] - data->x_to_find, 2) + pow(table.table[i].table[j][0] - data->y_to_find, 2) + pow(table.table[i].table[0][0] - data->z_to_find, 2));
                if (ab < min)
                {

                }
            }
        }
    }
}