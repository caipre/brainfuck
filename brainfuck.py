#! /usr/bin/python3

class Brainfuck:

    debug   = False

    def __init__(self, cells=5):

        self.memory  = [0 for x in range(0, cells)]
        self.pointer = 0

        self.program = ""
        self.cursor  = 0

        self.syntax  = {
            '>' : self.forward,
            '<' : self.backward,
            '+' : self.increment,
            '-' : self.decrement,
            '.' : self.output,
            ',' : self.input,
            '[' : self.start_loop,
            ']' : self.stop_loop,
        }

    def token(self):
        return self.program[self.cursor]

    def execute(self, token):
        try: self.syntax[token]()
        except KeyError: pass

    def run(self, program):
        self.program = program
        print (self.program)
        while self.cursor < len(self.program):
            if self.debug:
                print ("Token: {0}  {1}".format(self.program[self.cursor], [m for m in self.memory]), end="")

            self.execute(self.token())

            if self.debug:
                print (" -> {0}".format([m for m in self.memory]))

            self.cursor += 1

    ## Operators
    def forward(self):
        if self.pointer < len(self.memory)  - 1:
            self.pointer += 1
        else:
            exit("Fatal Error: Index out of range")

    def backward(self):
        if self.pointer > 0:
            self.pointer -= 1
        else:
            exit("Fatal Error: Index out of range")

    def increment(self):
        self.memory[self.pointer] += 1

    def decrement(self):
        self.memory[self.pointer] -= 1

    def output(self):
        print(chr(self.memory[self.pointer]), end="")

    def input(self):
        try: self.syntax[input()]()
        except KeyError: pass

    def start_loop(self):
        if self.memory[self.pointer] == 0:
            try: self.cursor = self.program.index("]", self.cursor)
            except ValueError: exit("Fatal Error: Unmatched '[' at position {0}".format(self.cursor))

    def stop_loop(self):
        bracket = 0
        if self.memory[self.pointer] != 0:
            for c in range(self.cursor-1, -1, -1):
                t = self.program[c]
                if t == ']':
                    bracket += 1
                elif t == '[':
                    if bracket > 0:
                        bracket -= 1
                    else:
                        self.cursor = c
                        return

            if bracket > 0:
                exit("Fatal Error: Unmatched ']' at position {0}".format(self.cursor))


if __name__ == '__main__':
    bf = Brainfuck()
    #bf.run("+++[>+<-]>>+")
    bf.run("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
