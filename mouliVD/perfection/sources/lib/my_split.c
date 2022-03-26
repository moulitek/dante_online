/*
** EPITECH PROJECT, 2022
** my_split
** File description:
** my_split
*/

#include <stddef.h>
#include <stdlib.h>

int get_strlen(char *str)
{
    int i;
    for (i = 0; str[i++];);
    return i;
}

int get_len_of_word(char *str, int i, char del, char del2)
{
    int b;
    for (b = i; str[i] != del && str[i] != del2
    && str[i] != '\0'; i++);
    return i - b;
}

char **my_split(char *str, char del, char del2)
{
    int i;
    int o = 0;
    int u = 0;
    char **result = malloc(sizeof(char *) * (get_strlen(str)));
    for (i = 0; str[i]; i++) {
        for (; (str[i] == del || str[i] == del2)
        && str[i] != '\0'; i++);
        result[o] = malloc(sizeof(char) *
        (get_len_of_word(str, i, del, del2) + 1));
        for (u = 0; (str[i] != del && str[i] != del2)
        && str[i] != '\0'; result[o][u++] = str[i], i++);
        result[o++][u] = '\0';
        for (; (str[i] == del || str[i] == del2)
        && str[i] != '\0'; i++);
        i--;
    }
    result[o] = NULL;
    return result;
}
