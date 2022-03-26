/*
** EPITECH PROJECT, 2022
** MazeComplexityEvalutation
** File description:
** my_lens
*/

#include "complexity.h"

int my_strlen(char *str)
{
    int i;
    for (i = 0; str[i]; i++);
    return i;
}

int my_tablen(char **str)
{
    int i;
    for (i = 0; str[i]; i++);
    return i;
}
