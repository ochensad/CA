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

    int comand;
    newton_polynomial newton;
    newton.diff_table.table = NULL;
    newton.x_values = NULL;
    newton.diff_table.rows = 0;

    hermit_polynomial hermit;
    hermit.diff_table.table = NULL;
    hermit.x_values = NULL;
    hermit.diff_table.rows = 0;

    int flag = 1;
    while(flag)
    {
        error_code = read_comand(&comand);
        if (error_code)
        {
            for (int i = 0; i < func_table.size; i++)
                free_table(func_table.table[i].table, func_table.table[i].rows);
            free(func_table.table);
            return error_code;
        }

        else if (comand == 0)
        {
            flag = 0;
        }
    }
    for (int i = 0; i < func_table.size; i++)
        free_table(func_table.table[i].table, func_table.table[i].rows);
    free(func_table.table);
    free_table(newton.diff_table.table, newton.diff_table.rows);
    free_table(hermit.diff_table.table, hermit.diff_table.rows);
    return OK;
}