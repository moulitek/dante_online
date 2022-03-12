import sys
from termcolor import colored

file_opened = open("./"+sys.argv[1], 'r')
str = file_opened.read()
big = str.split("\n")
len = len(big[0])
print(colored(" |", "magenta"), end="")
for i in range(len):
    print(colored("-", "magenta"), end="")
print(colored("|\n |", "magenta"), end="")
for i in str:
    if i == 'X':
        print(colored(i, "red"), end="")
    elif i == 'o':
        print(colored(i, "green"), end="")
    elif i == '*':
        print(colored(i, "yellow"), end="")
    elif i == '\n' or i == '\0':
        print(colored("| ", "magenta") + "\n" +
              colored(" |", "magenta"), end="")
print(colored("|", "magenta"))
print(colored(" |", "magenta"), end="")
for i in range(len):
    print(colored("-", "magenta"), end="")
print(colored("|", "magenta"))
