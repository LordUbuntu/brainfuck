from fileinput import input as filein

# from sys import stdin, stdout


# instantiate the tape
class machine:
    def __init__(self):
        self.head = 0
        self.tape = [0] * 30_000

    # TODO should turing machine wrap-around? how about an infinite tape off to the right, but no moving further left than tile 0
    # TODO take input as a string and parse into a buffer represented as an array of chars (whose value is modulo'd to keep in UTF range). Additional inputs can be parsed and (added onto? replace?) the current buffer stack.
    # eg:
    #   buffer = [char for char in stdin.readline().strip("\n")]
    #       maybe buffer = [ord(char) for char in ^^^]
    #   ord(buffer.pop(0))  # FIFO

    def inc(self):
        self.tape[self.head] += 1 % 0b11111111

    def dec(self):
        self.tape[self.head] -= 1 % 0b11111111

    def mvr(self):
        self.head += 1 % len(self.tape)

    def mvl(self):
        self.head -= 1 % len(self.tape)

    def show(self):
        print(chr(self.tape[self.head] % 0x10FFFF))

    def read(self):
        self.tape[self.head] = ord(input("In: ")[0]) % 0x10FFFF


def parse():
    raw_input = [char for line in filein() for char in line]
    program = []
    for char in raw_input:
        if char in ["+", "-", ">", "<", ",", ".", "[", "]"]:
            program.append(char)
    return program


def interpret(program):
    M = machine()
    index = 0
    loop_index = []

    while index < len(program):
        char = program[index]
        if char == "+":
            M.inc()
        if char == "-":
            M.dec()
        if char == ">":
            M.mvr()
        if char == "<":
            M.mvl()
        if char == ".":
            M.show()
        if char == ",":
            M.read()
        if char == "[":
            loop_index.append(index)
        if char == "]":
            if len(loop_index) > 0:
                if M.tape[M.head] == 0:
                    loop_index.pop()
                else:
                    index = loop_index[-1]
            else:
                # no matching [ implied
                print(f"ERROR: mismatching ], command #{index}")
        if char == "#":
            # special debugger symbol in some implementations
            print(f"{M.tape[:10]} {M.head}")
        index += 1


def main():
    interpret(parse())


main()

# maybe repeat by pushing every char for a range into a list, and then parsing that list repeatedly until the value of the tape at the head is 0 at the end of that list
