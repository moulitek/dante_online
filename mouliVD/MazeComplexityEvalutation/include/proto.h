/*
** EPITECH PROJECT, 2021
** project name
** File description:
** simple description
*/

#ifndef PROTO_H_
    #define PROTO_H_

int main(int ac, char **ag);
int check_error(int ac, char **ag);
int get_strlen(char *str);
int get_len_of_word(char *str, int i, char del, char del2);
char **my_split(char *str, char del, char del2);
int my_strlen(char *str);
int my_tablen(char **str);
void display_map(char **map);
int check_perfect(char **map, int x, int y, int height, int length, int y_from, int x_from);
int calculate_complexity(int ac, char **ag);
char *get_file_content(char *file_name);

#endif /* PROTO_H_ */
