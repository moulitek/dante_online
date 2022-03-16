##
## EPITECH PROJECT, 2022
## MazeComplexityEvalutation
## File description:
## Makefile
##

SRC	=	$(wildcard sources/*.c) $(wildcard sources/*/*.c) main.c

OBJ	=	$(SRC:.c=.o)

CFLAGS	=	-I./include -O2

NAME	=	checkPerfect

all:	$(NAME)

$(NAME):	$(OBJ)
	gcc -o $(NAME) $(OBJ) $(CFLAGS)

clean:
	rm -f $(OBJ)

fclean:	clean
	rm -f $(NAME)

re:	fclean	all
