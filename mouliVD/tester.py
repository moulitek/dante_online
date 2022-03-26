#!/bin/python3
import os
from time import sleep
from moulitek.moulitek import *

sequences = {
    "bad_char": ("Bad characters", "Mazes with wrong characters."),
    "bad_lines": ("Wrong lines length", "Mazes with wrong line length."),
    "empty": ("Empty maze", "Empty maze file."),
    "no_solution": ("No solution", "Mazes without solution."),
    "return_line": ("Line break", "Mazes with line break at the end."),
}

tests = {
    "bad_carac1": ("Bad character 1", "'#' character at every end of lines."),
    "bad_carac2": ("Bad character 2", "'p' character at the bottom of the maze."),
    "bad_carac3": ("Bad character 3", "'D' and 'µ' everywhere."),
    "bad_nbline1": ("Short line at the end", "Last line is shorter."),
    "bad_nbline2": ("Long line at the beginning", "Second line is longer."),
    "bad_nbline3": ("Short line at the beginning", "Second line is shorter."),
    "empty_maze": ("Empty maze", "Empty maze."),
    "no_escape": ("No escape", "The end is surrounded by walls."),
    "only_X": ("Only X", "The maze is only composed of a single 'X'."),
    "start_with_X": ("Start with X", "The maze starts with a 'X'."),
    "end_with_X": ("End with X", "The maze ends with a 'X'."),
    "end_with_return_line": ("End with line break", "The maze ends with a line break."),
}

solver_sequences = {
    "small_perfect": ("Small perfect maze", "Perfect maze of size 10x10."),
    "small_imperfect": ("Small imperfect maze", "Imperfect maze of size 10x10."),
    "medium_perfect": ("Medium perfect maze", "Perfect maze of size 100x100."),
    "medium_imperfect": ("Medium imperfect maze", "Imperfect maze of size 100x100.")
}

generation_sequences = [
    ("Small Mazes", "Mazes with a small size."),
    ("Medium Mazes", "Mazes with a medium size."),
    ("Big Mazes", "Mazes with a big size.")
]


def manage_exit(sequence, test, exitstat, expected, timeout):
    if exitstat == expected:
        sequence.set_status(test, True)
        return True
    elif exitstat == 124:
        sequence.set_status(test, False, TIMEOUT,
                            expected="Exit status %d" % expected, got="Timeout after %ds" % timeout)
        return False
    elif exitstat == 139:
        sequence.set_status(test, False, SEGFAULT,
                            expected="Exit status %d" % expected, got="Segmentation fault")
        return False
    else:
        sequence.set_status(test, False,
                            RETVALUE, expected=str(expected), got=str(exitstat))
        return False


generation_tests = [
    [
        ("1*1", 1, 1),
        ("2*2", 2, 1),
        ("10*10", 10, 2)
    ],
    [
        ("100*100", 100, 3),
        ("1000*1000", 1000, 5),
        ("5000*5000", 5000, 7)
    ],
    [
        ("10000*10000", 10000, 20),
        ("30000*30000", 30000, 30),
        ("50000*50000", 50000, 40)
    ]
]
error_handling_generation_sequences = [
    ("Bad dimensions", "Executing generator with invalid dimensions."),
    ("Bad arguments", "Executing generator with non-numerics arguments."),
    ("Bad argument count", "Executing generator with too few/much arguments."),
]
error_handling_generation_tests = [
    [
        ["0", "2"],
        ["2", "0"],
        ["0", "0"],
        ["2", "-0"],
        ["-2", "0"],
        ["2", "-2"],
        ["-2", "-2"]
    ],
    [
        ["a", "2"],
        ["2", "a"],
        ["z", "2"],
        ["2", "z"],
        ["2Ab", "0"],
        ["A", "2"],
        ["a", "a"],

    ],
    [
        ["2"],
        ["2", "2", "perfect", "imperfect"]
    ]
]

init_moulitek()
os.system("cd mouliVD/perfection && timeout 10s make re > /dev/null && mv checkPerfect ../../ && cd ../../")

generation_eh = Category("Generation - Error Handling",
                         "Generation error handling tests.")
for i, seq in enumerate(error_handling_generation_sequences):
    sequence = generation_eh.add_sequence(seq[0], seq[1])
    for j, test in enumerate(error_handling_generation_tests[i]):
        sequence.add_test("%s #%d" % (seq[0], j + 1),
                          "Command : generator/generator %s" % " ".join(test))
        exitstat = call_system("generator/generator %s" %
                               " ".join(test), timeout=5)
        manage_exit(sequence, "%s #%d" % (seq[0], j + 1), exitstat, 84, 5)

generation_time = Category(
    "Generation - Time", "Time to generate a maze of different sizes.")
for i, seq in enumerate(generation_sequences):
    sequence = generation_time.add_sequence(seq[0], seq[1])
    for j, test in enumerate(generation_tests[i]):
        sequence.add_test("%s in %ds" % (test[0], test[2]))
        exitstat = call_system(
            "generator/generator %d %d" % (test[1], test[1]), timeout=test[2])
        manage_exit(sequence, "%s in %ds" %
                    (test[0], test[2]), exitstat, 0, test[2])

generation_perfection = Category(
    "Generation - Perfection", "Checking if your mazes are perfects.")
for perfection in ["", "perfect"]:
    for x in range(2):
        for y in range(2):
            sequence = generation_perfection.add_sequence("%s - (%s width - %s height)" % ("Perfect" if perfection == "perfect" else "Imperfect", "odd" if x %
                                                          2 else "even", "odd" if y % 2 else "even"), ("Checking if your programm produce %s maze." % ("a perfect" if perfection == "perfect" else "an imperfect")))
            for i in range(5):
                test_name = "%s #%d" % (
                    "Perfect" if perfection == "perfect" else "Imperfect", i + 1)
                sequence.add_test(test_name, "Maze of %d*%d (%s)" % (
                    50 + x, 50 + y, "perfect" if perfection == "perfect" else "imperfect"))
                exitstat = call_system(
                    "generator/generator %d %d %s > maze" % (50 + x, 50 + y, perfection), timeout=10)
                if manage_exit(sequence, test_name, exitstat, 0, 10):
                    exitstat = call_system(
                        "./checkPerfect maze", timeout=10)
                    if (exitstat != 0 and perfection == "perfect") or (exitstat != 1 and perfection == ""):
                        if exitstat in range(2):
                            sequence.set_status(test_name, False, BADOUTPUT, expected="Perfect maze" if perfection ==
                                                "perfect" else "Imperfect maze", got="Imperfect maze" if perfection == "perfect" else "Perfect maze")
                        else:
                            sequence.set_status(
                                test_name, False, BADOUTPUT, expected="Perfect maze" if perfection == "perfect" else "Imperfect maze", got="Unknown error")

generation_complexity = Category(
    "Generation - Complexity", "Checking if your mazes are complex enough.")
sequence = generation_complexity.add_sequence(
    "Perfect Complexity", "Checking if your perfect mazes are complex enough.")
for i in range(10):
    test_name = "Perfect #%d" % (i + 1)
    sequence.add_test(test_name, "Maze of 50*50 (perfect)")
    exitstat = call_system(
        "generator/generator 50 50 perfect > maze", timeout=10)
    if manage_exit(sequence, test_name, exitstat, 0, 10):
        exitstat = call_system(
            "python3 mouliVD/evaluate_complexity.py maze", timeout=10)
        if exitstat == 0:
            sequence.set_status(test_name, True)
        elif exitstat == 2:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough straight aways")
        elif exitstat == 3:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough junctions")
        elif exitstat == 4:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough dead ends")
        else:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Unknown error")

sequence = generation_complexity.add_sequence(
    "Imperfect Complexity", "Checking if your imperfect mazes are complex enough.")
for i in range(10):
    test_name = "Imperfect #%d" % (i + 1)
    sequence.add_test(test_name, "Maze of 50*50 (imperfect)")
    exitstat = call_system("generator/generator 50 50 > maze", timeout=10)
    if manage_exit(sequence, test_name, exitstat, 0, 10):
        exitstat = call_system(
            "python3 mouliVD/evaluate_complexity.py maze", timeout=10)
        if exitstat == 0:
            sequence.set_status(test_name, True)
        elif exitstat == 2:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough straight aways")
        elif exitstat == 3:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough junctions")
        elif exitstat == 4:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Not enough dead ends")
        else:
            sequence.set_status(test_name, False, BADOUTPUT,
                                expected="Complex maze", got="Unknown error")

solver_eh = Category("Solver - Error Handling",
                     "Cheking the error handling of the solver part.")
for directory in os.listdir("mouliVD/map"):
    sequence = solver_eh.add_sequence(
        sequences[directory][0], sequences[directory][1])
    for file in os.listdir("mouliVD/map/" + directory):
        sequence.add_test(tests[file][0], tests[file][1])
        exitstat = call_system(
            "solver/solver " + "mouliVD/map/" + directory + "/" + file, timeout=10)
        manage_exit(sequence, tests[file][0], exitstat, 84, 10)

solver = Category("Solver", "Checking if your solver is working.")
for directory in solver_sequences:
    seq = solver_sequences[directory]
    sequence = solver.add_sequence(seq[0], seq[1])
    for i, file in enumerate(os.listdir("mouliVD/solver/" + directory)):
        sequence.add_test("%s #%d" % (seq[0], i + 1))
        exitstat = call_system(
            "solver/solver " + "mouliVD/solver/" + directory + "/" + file + " > solved", timeout=10)
        if manage_exit(sequence, "%s #%d" % (seq[0], i + 1), exitstat, 0, 10):
            exitstat = call_system("python3 mouliVD/is_solved.py %s solved" % (
                "mouliVD/solver/" + directory + "/" + file), timeout=10)
            manage_exit(sequence, "%s #%d" % (seq[0], i + 1), exitstat, 0, 10)

gen_trace()
