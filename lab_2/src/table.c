#include "table.h"
#include "errors.h"
#include "struct.h"
#include <stdlib.h>
#include <stdio.h>

void free_table(double **table, int n)
{
    for(int i = 0; i < n; i++)
        free(table[i]);
    free(table);
}

int allocate_table(table_t *table)
{
    double **data = calloc(table->rows,sizeof(double*));
    if (!data)
        return ERROR_MEMORY;
    for (int i = 0; i < table->rows; i++)
    {
        data[i] = malloc(table->columns * sizeof(double));
        if (!data[i])
        {
            free_table(data, table->rows);
            return ERROR_MEMORY;
        }
    }
    table->table = data;
    return OK;
}

int read_file(char *filename, table_arr_t *table)
{
    FILE *f;
    f = fopen(filename, "r");
    if (f == NULL)
    {
        printf("Ошбика открытия файла\n");
        return ERROR_OPEN_FILE;
    }
    int table_size;
    if (fscanf(f, "%d", &table_size) != 1)
    {
        printf("Ошибка чтения размера\n");
        return ERROR_READING;
    }
    if (table_size <= 0)
    {
        printf("Ошибка недопустимый размер\n");
        return ERROR_SIZE;
    }
    table->table = calloc(table_size, sizeof(table_t));
    table->size = table_size;
    for (int i = 0; i < table_size; i++)
    {
        fscanf(f, "%d %d", &table->table[i].rows, &table->table[i].columns);
        int error_code = allocate_table(&(table->table[i]));
        if (error_code)
        {
            printf("Ошибка выделения памяти\n");
            return error_code;
        }
        for (int j = 0; j < table->table[i].rows; j++)
        {
            for (int k = 0; k < table->table[i].columns; k++)
            {
                if (fscanf(f,"%lf", &(table->table[i].table[j][k])) == EOF)
                {
                    printf("Ошибка чтения");
                    return ERROR_READING;
                }
            }
        }
    }
    return OK;
}

void print_func_table(table_arr_t* table)
{
    printf("Полученные из файла данные\n");
    
    for (int i = 0; i < table->size; i++)
    {
        printf("При z = %.3lf\n", table->table[i].table[0][0]);
        for (int j = 0; j < table->table[i].rows; j++)
        {
            for(int k = 0; k < table->table[i].columns; k++)
            {
                if (k == 0 && j == 0)
                    printf("%6s", "y/x");
                else
                    printf("%6.3lf ", table->table[i].table[j][k]);
            }
            printf("\n");
        }
        printf("\n");
    }
    printf("\n\n");
}

void sort_table(table_t *table)
{
    double tmp_x;
    double tmp_y;
    double tmp_yy;
    for (int i = 0; i < table->rows; i++)
    {
        for (int j = 0; j < table->rows - i - 1; j++)
        {
            if (table->table[j][0] > table->table[j + 1][0])
            {
                tmp_x = table->table[j][0];
                tmp_y = table->table[j][1];
                tmp_yy = table->table[j][2];
                table->table[j][0] = table->table[j + 1][0];
                table->table[j][1] = table->table[j + 1][1];
                table->table[j][2] = table->table[j + 1][2];
                table->table[j + 1][0] = tmp_x;
                table->table[j + 1][1] = tmp_y;
                table->table[j + 1][2] = tmp_yy;
            }
        }
    }
}