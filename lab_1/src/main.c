#include "errors.h"
#include "struct.h"
#include <stdio.h>
#include "file_func.h"
#include "table.h"
#include "polynoms.h"

#define MAX_FILE_NAME_LEN 25

int main(void)
{
    setbuf(stdout, NULL);
    printf("Реализация алгоритма полиномиальной\n интерполяции табличных функций\n\n");

    table_t func_table;
    func_table.table = NULL;
    func_table.columns = 3;

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

    print_func_table(func_table);

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
            free_table(func_table.table, func_table.rows);
            return error_code;
        }

        if (comand == 1)
        {
            error_code = get_newton_polynomial(&newton, &func_table);
            if (error_code)
            {
                free_table(func_table.table, func_table.rows);
                free_table(newton.diff_table.table, newton.diff_table.rows);
                free_table(hermit.diff_table.table, hermit.diff_table.rows);
                return error_code;
            }
        }
        else if (comand == 2)
        {
            error_code = get_hermit_polynomial(&hermit, &func_table);
            if (error_code)
            {
                free_table(func_table.table, func_table.rows);
                free_table(newton.diff_table.table, newton.diff_table.rows);
                free_table(hermit.diff_table.table, hermit.diff_table.rows);
                return error_code;
            }
        }
        else if (comand == 3)
        {
            error_code = compare(&func_table);
            if (error_code)
            {
                free_table(func_table.table, func_table.rows);
                free_table(newton.diff_table.table, newton.diff_table.rows);
                free_table(hermit.diff_table.table, hermit.diff_table.rows);
                return error_code;
            }
        }
        else if (comand == 0)
        {
            flag = 0;
        }
    }
    free_table(func_table.table, func_table.rows);
    free_table(newton.diff_table.table, newton.diff_table.rows);
    free_table(hermit.diff_table.table, hermit.diff_table.rows);
    return OK;
}