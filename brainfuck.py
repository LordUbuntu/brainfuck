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
        if command == "[":
            # move ahead to nearest ] if value in tape is 0
            if tape[head] == 0:
                index = closing_bracket[index]
        elif command == "]":
            # move back to nearest [ if value in tape is not 0
            if tape[head] != 0:
                index = opening_bracket[index]
        elif command == "+":
            # increment value of tape at head (wrap overflow)
            tape[head] = (tape[head] + 1) % 256
        elif command == "-":
            # decrement value of tape at head (wrap underflow)
            tape[head] = (tape[head] - 1) % 256
        elif command == ">":
            # move head to next right tape, creating new tapes if necessary
            head += 1
            if head > len(tape):
                tape.append(0)
        elif command == "<":
            # move head to next left tape, do nothing it already at leftmost
            head -= 1
            if head < 0:
                head = 0
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
