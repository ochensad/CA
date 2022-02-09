#include "table.h"
#include "errors.h"
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

int read_file(char *filename, table_t *table)
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
    table->rows = table_size;
    int error_code = allocate_table(table);
    if (error_code)
    {
        printf("Ошибка выделения памяти\n");
        return error_code;
    }
    int i = 0;
    while (i < table_size && fscanf(f, "%lf %lf %lf", &table->table[i][0], &table->table[i][1], &table->table[i][2]) != EOF)
    {
        i++;
    }
    return OK;
}

void print_func_table(table_t table)
{
    printf("Полученные из файла данные\n");
    printf("%6s  %6s  %6s\n", "x", "y", "y'");
    for(int i = 0; i < table.rows; i++)
        printf("%lf %lf %lf\n", table.table[i][0], table.table[i][1], table.table[i][2]);
    printf("\n\n");
}