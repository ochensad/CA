#include "file_func.h"
#include "errors.h"
#include <stdio.h>

int read_file_name(char *name)
{
    int error_code;
    printf("\nВведите имя файла: ");
    error_code = scanf("%s", name);
    if (error_code != 1)
    {
        printf("Ошибка чтения имени файла\n");
        return ERROR_READING;
    }
    return OK;
}

int read_comand(int *comand)
{
    printf("Выберите действие:\n 1. Поиск значения y(x) с помощью полинома Ньютона\n   (Степень вводится с клавиатуры)\n\n 2. Поиск значения y(x) с помощью полинома Эрмита\n   (количество узлов вводится с клавиатуры)\n\n 3. Сравнение полиномов Ньютона и Эрмита в таблице\n\n 4. Найти корень табличной функции с помощью обратной интерполяции, \n    используя полином Ньютона\n\n 0. Выход\n\n");

    printf("Команда: ");
    if (scanf("%d", comand) != 1)
    {
        printf("\n");
        return ERROR_READING;
    }
    if (*comand < 0 || *comand > 4)
    {
        printf("\n");
        return ERROR_COMAND;
    }
    return OK;
}