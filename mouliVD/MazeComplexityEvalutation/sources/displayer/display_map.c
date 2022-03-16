/*
** EPITECH PROJECT, 2022
** MazeComplexityEvalutation
** File description:
** display_map
*/

#include "complexity.h"

void display_map(char **map)
{
    for (int i = 0; map[i]; printf("%s\n", map[i++]));
}