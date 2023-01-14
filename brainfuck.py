#!/bin/python3.9
# Jacobus Burger (2021)
# Jacobus Burger (2021)
# Info:
#   BrainFuck interpreter written in Python.
#   This implementation treats the input file as a program tape (think a
#   punch card) and executes command symbols across that program tape, moving
#   about it as the program is executed. The interpreter simultaneously
#   emulates a turing tape that records the state of the program as it is
#   being executed.
# See:
#   https://en.wikipedia.org/wiki/Brainfuck
#   https://esolangs.org/wiki/Brainfuck
#   https://www.youtube.com/watch?v=hdHjjBS4cs8
from sys import argv, stdin, stdout, exit
from operator import contains
from functools import partial


def main():
    # valid BF symbols/commands
    bf_commands = ['+', '-', '<', '>', ',', '.', '[', ']', '#']
    # Turing Machine Emulator
    tape = [0] * 30_000  # array of cells each holding an ascii value [0..255]
    head = 0  # current cell


    # read file at path specified as first argument
    try:
        with open(argv[1], "r") as file:
            # filter file for recognized BF commands only
            bf_program_filter = partial(contains, bf_commands)
            # NOTE: program is an array of BF symbols/commands (a program tape)
            program = list(filter(bf_program_filter, file.read()))
    # handle potential exceptions from reading in program
    except IndexError:
        exit("no file was provided!")
    except FileNotFoundError:
        exit(f"file '{argv[1]}' could not be found!")


    # validate program by ensuring no unmatched brackets
    bracket_symmetry = program.count('[') - program.count(']')
    if program.count('[') - program.count('[') != 0:
        exit("ERR: unmatched '[' or ']' in program")


    # execute program tape
    index = 0  # the index of the current command in the program
    skip = 0  # used to determine if and in which direction to loop [ and ]
    while index < len(program):
        # grab current command in program
        command = program[index]

        # execute the current command in the program
        if skip != 0:
            # skip to a matching bracket if skip is active
            # NOTE:
            #   What is depth and why are we using it?
            #   The [ and ] skip algorithm is pretty straightforward. Treat
            #   all [ like a 1 and all ] like a -1, then adding the values of
            #   the matching pairs will give us 0 (1 - 1 == 0). This way we
            #   can ignore commands and nested [ and ] between the start [
            #   and its matching ] assuming we're skipping forward. The logic
            #   to go backwards is the same but we just reverse the values
            #   so that [ is -1 and ] is 1.
            if skip == 1:
                # skip forward...
                # start on the command following calling [
                index += 1
                # skip forwards to command after matching ]
                depth = 1  # tracks matching brackets ([ = 1, ] = -1)
                while depth > 0:
                    command = program[index]
                    if command == '[':
                        depth += 1
                    elif command == ']':
                        depth -= 1
                    index += 1
                # end forward skip on command after ]
                skip = 0
                continue
            if skip == -1:
                # skip backwards...
                # start on the command before the calling ]
                index -= 1
                # skip backwards to the command after matching [
                depth = 1  # tracks matching brackets ([ = -1, ] = 1)
                while depth > 0:
                    # look at command ahead so we end on matching [
                    command = program[index - 1]
                    if command == '[':
                        depth -= 1
                    elif command == ']':
                        depth += 1
                    index -= 1
                # move to command after matching [
                index += 1
                # end backward skip on command after [
                skip = 0
                continue
        elif command == "[":
            # move ahead to command after matching ] if value in tape is 0
            if tape[head] == 0:
                skip = 1
                continue  # keeping index on the calling [
            # otherwise ignore the [ if value in tape is not 0
        elif command == "]":
            # move back to command after matching [ if value in tape is not 0
            if tape[head] != 0:
                skip = -1
                continue  # keeping index on the calling ]
            # otherwise ignore the ] if value in tape is 0
        elif command == "+":
            # increment value of tape at head (wrap overflow)
            tape[head] = (tape[head] + 1) % 256
        elif command == "-":
            # decrement value of tape at head (wrap underflow)
            tape[head] = (tape[head] - 1) % 256
        elif command == ">":
            # move head to right tape, stay if that would move off tape
            head += 1 if head + 1 < len(tape) else 0
        elif command == "<":
            # move head to left tape, stay if that would move off tape
            head -= 1 if head - 1 >= 0 else 0
        elif command == ",":
            # read 1 byte of input into current tape (as ordinal)
            line = stdin.readline()
            if len(line) == 0:
                tape[head] = 0  # default to 0 if input invalid
            else:
                tape[head] = ord(line[0]) % 256  # wraparound valid values
        elif command == ".":
            # write 1 byte of output from current cell (as ascii char)
            stdout.write(chr(tape[head]))
        elif command == "#":
            # debug: show state of first 10 cells of tape
            print(f"{head} {tape[:10]}")

        # move to next command in program tape
        index += 1


if __name__ == "__main__":
    main()  # 55 sloc for the whole interpreter
