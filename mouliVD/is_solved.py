import sys

if len(sys.argv) != 3:
    exit(1)

maze = [list(line) for line in open(sys.argv[1]).readlines()]
solved = [list(line) for line in open(sys.argv[2]).readlines()]

dims = (len(maze[0]), len(maze))

if dims[1] != len(solved) or dims[0] != len(solved[0]):
    exit(1)

coords = (0, 0)
while coords[0] != len(maze[0]) - 1 and coords[1] != len(maze) - 1:
    next_o = []
    solved[coords[1]][coords[0]] = 'f'
    for pos in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_coords = (coords[0] + pos[0], coords[1] + pos[1])
        if new_coords[0] not in range(dims[0]) or new_coords[1] not in range(dims[1]):
            continue
        if solved[new_coords[1]][new_coords[0]] == 'o':
            if maze[new_coords[1]][new_coords[0]] != '*':
                exit(1)
            next_o.append(new_coords)
    if len(next_o) != 1:
        exit(1)
    coords = next_o[0]