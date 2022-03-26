/*
** EPITECH PROJECT, 2022
** MazeComplexityEvalutation
** File description:
** complexity_evaluation
*/

#include "complexity.h"

int check_perfect(char **map, int x, int y, int height, int length, int y_from, int x_from)
{
    int output;
    if (x > 0) {
        if (map[y][x - 1] == '*') {
            map[y][x - 1] = 'f';
            if (check_perfect(map, x - 1, y, height, length, y, x) == 1)
                return 1;
        } else if (map[y][x - 1] == 'f' && !(y == y_from && x - 1 == x_from)) {
            return 1;
        }
    }
    if (y > 0) {
        if (map[y - 1][x] == '*') {
            map[y - 1][x] = 'f';
            if (check_perfect(map, x, y - 1, height, length, y, x) == 1)
                return 1;
        } else if (map[y - 1][x] == 'f' && !(y - 1 == y_from && x == x_from)) {
            return 1;
        }
    }
    if (y + 1 < height) {
        if (map[y + 1][x] == '*') {
            map[y + 1][x] = 'f';
            if (check_perfect(map, x, y + 1, height, length, y, x) == 1)
                return 1;
        } else if (map[y + 1][x] == 'f' && !(y + 1 == y_from && x == x_from)) {
            return 1;
        }
    }
    if (x + 1 < length) {
        if (map[y][x + 1] == '*') {
            map[y][x + 1] = 'f';
            if (check_perfect(map, x + 1, y, height, length, y, x) == 1)
                return 1;
        } else if (map[y][x + 1] == 'f' && !(y == y_from && x + 1 == x_from)) {
            return 1;
        }
    }
    return 0;
}

int calculate_complexity(int ac, char **ag)
{
    char *file_content;
    char **map;
    int length;
    int height;
    if (check_error(ac, ag) == 84)
        return 1;
    file_content = get_file_content(ag[1]);
    map = my_split(file_content, '\n', '\n');
    length = my_strlen(map[0]);
    height = my_tablen(map);
    if (map[height - 1][length - 1] != '*' || map[0][0] != '*')
        return 1;
    int output = check_perfect(map, 0, 0, height, length, 0, 1);
    if (output == 1)
        return 1;
    for (int i = 0; map[i]; i++) {
        for (int x = 0; map[i][x]; x++) {
            if (map[i][x] == '*')
                return 1;
        }
    }
    return 0;
}
