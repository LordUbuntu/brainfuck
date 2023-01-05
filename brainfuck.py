#!/bin/python3.9
# Jacobus Burger (2021)
# BrainFuck interpreter written in Python
#   For more info, see: https://en.wikipedia.org/wiki/Brainfuck
from sys import argv, stdin, stdout, exit
from operator import contains
from functools import partial


def main():
    # Turing Machine Emulator
    tape = [0] * 30_000  # array of cells each holding an ascii value [0..255]
    head = 0  # current cell
    # valid BF symbols/commands
    bf_commands = ['+', '-', '<', '>', ',', '.', '[', ']', '#']


    # read program from given file
    try:
        with open(argv[1], "r") as file:
            # filter file for recognized BF commands only
            bf_program_filter = partial(contains, bf_commands)
            # NOTE: program is an array of BF symbols/commands
            program = list(filter(bf_program_filter, file.read()))
    # handle potential exceptions
    except IndexError:
        exit("no file was provided!")
    except FileNotFoundError:
        exit(f"file '{argv[1]}' could not be found!")


    # validate the program by ensuring no unmatched brackets as precondition
    bracket_symmetry = program.count('[') - program.count(']')
    if program.count('[') - program.count('[') != 0:
        exit("ERR: unmatched '[' or ']' in program")

    # run the program
    index = 0  # the index of the current command in the program
    skip = 0  # used to determine if and in which direction to loop [ and ]
    while index < len(program):
        # grab current command in program
        command = program[index]

        # execute the current command in the program
        if skip != 0:
            # skip to a matching bracket if skip is active
            # what is depth and why are we using it?
            #   the [ and ] skip algorithm is pretty straightforward. Treat
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
