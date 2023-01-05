#!/bin/python3.9
# Jacobus Burger (2021)
# BrainFuck interpreter written in Python
#   For more info, see: https://en.wikipedia.org/wiki/Brainfuck
from sys import argv, stdin, stdout, exit
from operator import contains
from functools import partial


def main():
    # Turing Machine Emulator
    tape = [0] * 30_000  # array of tapes (the tape)
    head = 0  # current tape (the head)

    # BF symbols
    bf_commands = ['+', '-', '<', '>', ',', '.', '[', ']', '#']


    # read program from given file
    try:
        with open(argv[1], "r") as file:
            # filter file for recognized BF commands
            bf_program_filter = partial(contains, bf_commands)
            program = list(filter(bf_program_filter, file.read()))
    # handle potential exceptions
    except IndexError:
        exit("no file was provided!")
    except FileNotFoundError:
        exit(f"file '{argv[1]}' could not be found!")


    # validate the program by ensuring no unmatched brackets
    bracket_symmetry = program.count('[') - program.count(']')
    if program.count('[') - program.count('[') != 0:
        exit("ERR: unmatched '[' or ']' in program")

    # and record positions of opening and closing brackets
    opening_indices = []
    closing_bracket = {}
    for index, char in enumerate(program):
        if char == "[":
            opening_indices.append(index)
        elif char == "]":
            if len(opening_indices) == 0:
                exit(f"ERR: orphan ']' (command {index+1})!")
            closing_bracket[opening_indices.pop()] = index
    if len(opening_indices) > 0:
        exit(f"ERR: orphan '[' (command {opening_indices.pop()+1})!")
    opening_bracket = {v: k for k, v in closing_bracket.items()}


    # run the program
    index = 0  # the index of the current command in the program
    skip = 0  # used to determine if and in which direction to skip
    while index < len(program):
        # grab current command in program
        command = program[index]

        # execute the current command in the program
        if skip != 0:
            # skip to a matching bracket
            if skip == 1:
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
            # move ahead to command after matching ] if value in cell is 0
            if cell[head] == 0:
                skip = 1
                continue  # keeping index on the calling [
            # otherwise ignore the [ if value in cell is not 0
        elif command == "]":
            # move back to command after matching [ if value in cell is not 0
            if cell[head] != 0:
                skip = -1
                continue  # keeping index on the calling ]
            # otherwise ignore the ] if value in cell is 0
        elif command == "+":
            # increment value of tape at head (wrap overflow)
            tape[head] = (tape[head] + 1) % 256
        elif command == "-":
            # decrement value of tape at head (wrap underflow)
            tape[head] = (tape[head] - 1) % 256
        elif command == ">":
            # move head to right cell, stay if that would move off tape
            head += 1 if head + 1 < len(cell) else 0
        elif command == "<":
            # move head to left cell, stay if that would move off tape
            head -= 1 if head - 1 >= 0 else 0
        elif command == ",":
            # read 1 byte of input into current tape (as ordinal)
            line = stdin.readline()
            if len(line) == 0:
                exit(0)
            tape[head] = ord(line[0]) % 256
        elif command == ".":
            # write 1 byte of output from current tape (as char)
            stdout.write(chr(tape[head]))
        elif command == "#":
            # debug: show state of FSM
            print(f"{head} {tape[:10]}")

        # move to next command in sequence
        index += 1


if __name__ == "__main__":
    main()  # 55 sloc for the whole interpreter
