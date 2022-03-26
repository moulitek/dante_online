/*
** EPITECH PROJECT, 2022
** MazeComplexityEvalutation
** File description:
** check_error
*/

#include "complexity.h"

int check_error(int ac, char **ag)
{
    int fd;
    char buffer[10];
    if (ac != 2)
        return 84;
    if ((fd = open(ag[1], O_RDONLY)) <= 0)
        return 84;
    if(read(fd, buffer, 9) <= 0)
        return 84;
    return 0;
}
