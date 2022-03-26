import sys


def display_map(map):
    for lines in map:
        print(''.join(lines))


def calculate_dead_end(map, y, x):
    global dead_end
    global total_no_dead_end
    total_no_dead_end += 1
    i = 0
    if x + 1 < len(map[0]):
        if map[y][x + 1] == '*':
            map[y][x + 1] = 'L'
            calculate_dead_end(map, y, x + 1)
            i += 1
    if x > 0:
        if map[y][x - 1] == '*':
            map[y][x - 1] = 'L'
            calculate_dead_end(map, y, x - 1)
            i += 1
    if y + 2 < len(map):
        if map[y + 1][x] == '*':
            map[y + 1][x] = 'L'
            calculate_dead_end(map, y + 1, x)
            i += 1
    if y > 0:
        if map[y - 1][x] == '*':
            map[y - 1][x] = 'L'
            calculate_dead_end(map, y - 1, x)
            i += 1
    if i == 0:
        dead_end += 1


def calculate_straight_aways(map):
    id = 0
    tot = 0
    tot_all = 0
    for lines in map:
        if id >= 1 and id + 2 < len(map):
            for x in range(1, len(lines) - 2, 1):
                if (lines[x - 1: x + 1] == "***") and map[id - 1][x] == 'X' and map[id + 1][x] == 'X':
                    tot += 1
                if map[id - 1][x] == '*' and map[id + 1][x] == '*' and map[id][x + 1] == 'X' and map[id][x - 1] == 'X':
                    tot += 1
        tot_all += str(lines).count('*')
        id += 1
    return round(tot / tot_all * 100, 2)


def calculate_junctions_purcent(map):
    nbr = 0
    tot = 0
    for y in range(1, len(map) - 2, 1):
        tot += map[y].count("*")
        for x in range(1, len(map[y]) - 2, 1):
            if map[y][x] == '*' and ((map[y - 1][x] == '*' and (map[y][x - 1] == '*' or map[y][x + 1] == '*')) or map[y + 1][x] == '*' and (map[y][x - 1] == '*' or map[y][x + 1] == '*')):
                nbr += 1
    return round(nbr / tot * 100, 2)


def display_dead_end(map):
    global dead_end
    global total_no_dead_end
    total_no_dead_end = 0
    dead_end = 0
    stats = [calculate_straight_aways(map) > 20,
           calculate_junctions_purcent(map) > 20]
    calculate_dead_end(map, 0, 0)
    stats.append(round(dead_end/total_no_dead_end * 100, 2) > 20)
    if all(stats):
        exit(0)
    elif not stats[0]:
        exit(2)
    elif not stats[1]:
        exit(3)
    elif not stats[2]:
        exit(4)


def display_complexity():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        exit(1)
    filename = sys.argv[1]
    inside = [list(line) for line in open(filename, "r").read().split("\n")]
    display_dead_end(inside)


if __name__ == '__main__':
    display_complexity()
