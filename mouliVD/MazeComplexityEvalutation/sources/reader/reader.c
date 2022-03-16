/*
** EPITECH PROJECT, 2022
** MazeComplexityEvalutation
** File description:
** reader
*/

#include "complexity.h"

char *get_file_content(char *file_name)
{
    struct stat f;
    stat(file_name, &f);
    char *buffer = malloc(sizeof(char) * (f.st_size + 1));
    int fd = open(file_name, O_RDONLY);
    int len = read(fd, buffer, f.st_size);
    buffer[len] = 0;
    return buffer;
}
