#include "errors.h"
#include "struct.h"
#include <stdio.h>
#include "file_func.h"
#include "table.h"
#include "polynoms.h"
#include <stdlib.h>

#define MAX_FILE_NAME_LEN 25

int main(void)
{
    setbuf(stdout, NULL);
    printf("Реализация алгоритма полиномиальной\n интерполяции табличных функций\n\n");

    table_arr_t func_table;

    char filename[MAX_FILE_NAME_LEN + 1];
    int error_code = read_file_name(filename);
    if (error_code)
        return error_code;
    
    error_code = read_file(filename, &func_table);
    if (error_code)
    {
        printf("%d", error_code);
        return error_code;
    }
    //sort_table(&func_table);
    print_func_table(&func_table);

    n_exp n;
    printf("Введите степени nx, ny, nz: ");
    if (scanf("%d %d %d", &n.n_x, &n.n_y, &n.n_z) != 3)
    {
        printf("Ошибка чтения\n");
        for (int i = 0; i < func_table.size; i++)
            free_table(func_table.table[i].table, func_table.table[i].rows);
        free(func_table.table);
        return ERROR_READING;
    }
    data_t data;
    printf("\nВведите значения для поиска x, y, z: ");
    if (scanf("%lf %lf %lf", &data.x_to_find, &data.y_to_find, &data.z_to_find) != 3)
    {
        printf("Ошибка чтения\n");
        for (int i = 0; i < func_table.size; i++)
            free_table(func_table.table[i].table, func_table.table[i].rows);
        free(func_table.table);
        return ERROR_READING;
    }

    get_points(func_table, data);

    for (int i = 0; i < func_table.size; i++)
        free_table(func_table.table[i].table, func_table.table[i].rows);
    free(func_table.table);
    return OK;
}