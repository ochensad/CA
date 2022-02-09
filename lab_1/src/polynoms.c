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
    int error_code;

    printf("Введите степень полинома: ");
    if (scanf("%d", &newton->polynom_exp) != 1 || newton->polynom_exp < 1)
    {
        printf("Ошибка чтения\n");
        return ERROR_READING;
    }

    printf("Введите значение для поиска: ");
    if (scanf("%lf", &newton->value_to_find) != 1)
    {
        printf("Ошибка чтения\n");
        return ERROR_READING;
    }

    int i_find = find_index_in_table(newton->value_to_find, func_table);

    error_code = find_value_to_newton_table(newton, func_table, i_find);
    if (error_code)
        return error_code;
    
    fill_newton_table(newton);
    print_table(newton);
    count_newton_polynomial(newton);
    printf("Значение y(x): %lf\n", newton->y_value);
    return OK;
}

int find_value_to_hermit_table(hermit_polynomial *hermit, const table_t *func_table, int i_find)
{
    int get_left;
    int get_right;
    if (hermit->node_num / 2 > (i_find + 1))
    {
        get_left = i_find + 1;
        get_right = hermit->node_num - get_left;
    }
    else if (hermit->node_num / 2 > (func_table->rows - i_find))
    {
        get_right = func_table->rows - i_find - 1;
        get_left = hermit->node_num - get_right;
    }
    else
    {
        get_left = hermit->node_num / 2;
        get_right = hermit->node_num - get_left;
    }

    hermit->diff_table.rows = 2 * hermit->node_num;
    hermit->diff_table.columns = 2 * hermit->node_num;
    int error_code = allocate_table(&hermit->diff_table);
    if (error_code)
    {
        printf("Ошибка выделения памяти\n");
        return error_code;
    }

    hermit->x_values = calloc(2 * hermit->node_num, sizeof(double));
    if (hermit->x_values == NULL)
    {
        printf("Ошибка выделения памяти\n");
        return ERROR_MEMORY;
    }

    int j = 0;
    for (int i = 0; i < func_table->rows; i++)
    {
        if ((i >= i_find - get_left + 1) && (i <= i_find + get_right))
        {
            hermit->diff_table.table[j][0] = func_table->table[i][1];
            hermit->x_values[j] = func_table->table[i][0];
            hermit->diff_table.table[j][1] = func_table->table[i][2];
            j++;
            hermit->diff_table.table[j][0] = func_table->table[i][1];
            hermit->x_values[j] = func_table->table[i][0];
            j++;
        }
    }
    return OK;
}

void fill_hermit_table(hermit_polynomial *hermit)
{
    double x;
    for (int j = 0; j < hermit->node_num * 2 - 1; j++)
    {
        for (int i = 0; i < (hermit->node_num * 2 - 1) - j; i++)
        {
            if (j == 0 && i % 2 == 0)
                x = hermit->diff_table.table[i][j + 1];
            else
                x = (hermit->diff_table.table[i][j] - hermit->diff_table.table[i + 1][j]) / (hermit->x_values[i] - hermit->x_values[i + 1 + j]);
            printf("%lf ", x);
            hermit->diff_table.table[i][j + 1] = x;
        }
        printf("|%d|\n", j);
    }
}

void count_hermit_polynomial(hermit_polynomial *hermit)
{
    double value = 0;
    double buf = 1;
    double x_value = 0;
    for(int i = 0; i < hermit->node_num * 2; i++)
    {
        x_value = hermit->diff_table.table[0][i];
        for (int j = 0; j < i; j++)
        {
            buf *= (hermit->value_to_find - hermit->x_values[j]);
        }
        value += (x_value * buf);
        buf = 1;
        x_value = 0;
    }
    hermit->y_value = value;
}

void print_hermit_table(hermit_polynomial *hermit)
{
    printf("Таблица разностей\n\n");
    for(int i = 0; i < hermit->node_num * 2; i++)
    {
        for(int j = 0; j < hermit->node_num * 2 - i; j++)
            printf(" %lf", hermit->diff_table.table[i][j]);
        printf("\n");
    }
}

int get_hermit_polynomial(hermit_polynomial *hermit, const table_t *func_table)
{
    int error_code;

    printf("Введите количество узлов: ");
    if (scanf("%d", &hermit->node_num) != 1 || hermit->node_num < 1)
    {
        printf("Ошибка чтения\n");
        return ERROR_READING;
    }
    hermit->polynom_exp = hermit->node_num + 1;
    printf("Введите значение для поиска: ");
    if (scanf("%lf", &hermit->value_to_find) != 1)
    {
        printf("Ошибка чтения\n");
        return ERROR_READING;
    }

    int i_find = find_index_in_table(hermit->value_to_find, func_table);

    error_code = find_value_to_hermit_table(hermit, func_table, i_find);
    if (error_code)
        return error_code;
    fill_hermit_table(hermit);
    print_hermit_table(hermit);
    count_hermit_polynomial(hermit);
    printf("Значение y(x): %lf\n", hermit->y_value);
    printf("Степень полинома: %d\n", hermit->polynom_exp);
    return OK;
}


int compare(table_t *table)
{
    newton_polynomial newton;
    newton.diff_table.table = NULL;
    newton.x_values = NULL;

    hermit_polynomial hermit;
    hermit.diff_table.table = NULL;
    hermit.x_values = NULL;

    for(int i = 0; i < 4; i++)
    {
        
    }
    return OK;
}