#! /usr/bin/env python
import time

class Brainfuck:

    debug = False
    out_string = ""
    in_string = ""

    def __init__(self, cells=20):

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
            #print ("\r{0}^".format(" " * self.cursor), end="")

            if self.debug:
                print ("Token: {0}  {1}".format(self.program[self.cursor], [m for m in self.memory]), end="")

            self.execute(self.token())

            if self.debug:
                print (" -> {0}".format([m for m in self.memory]))

            self.cursor += 1
            #time.sleep(.01)

        if self.out_string:
            print(self.out_string)


    ## Operators
    def forward(self):
        if self.pointer < len(self.memory)  - 1:
            self.pointer += 1
        else:
            exit("Fatal Error: Index out of range (high)")

    def backward(self):
        if self.pointer > 0:
            self.pointer -= 1
        else:
            exit("Fatal Error: Index out of range (low)")

    def increment(self):
        self.memory[self.pointer] += 1

    def decrement(self):
        self.memory[self.pointer] -= 1

    def output(self):
        self.out_string += chr(self.memory[self.pointer])
        #print(chr(self.memory[self.pointer]), end="")

    def input(self):
        while not self.in_string:
            self.in_string = input()
            if self.in_string == "":
                break

        h = self.in_string[0:1]

        if h == "":
            self.memory[self.pointer] = -1
        else:
            self.in_string = self.in_string[1:]
            self.memory[self.pointer] = ord(h)

    def start_loop(self):
        if self.memory[self.pointer] == 0:
            brackets = 0
            for c in range(self.cursor+1, len(self.program)):
                t = self.program[c]
                if t == '[':
                    brackets += 1
                elif t == ']':
                    if brackets > 0:
                        brackets -= 1
                    else:
                        self.cursor = c
                        return

            exit("Fatal Error: Unmatched '[' at position {0}".format(self.cursor))

    def stop_loop(self):
        if self.memory[self.pointer] != 0:
            brackets = 0
            for c in range(self.cursor-1, -1, -1):
                t = self.program[c]
                if t == ']':
                    brackets += 1
                elif t == '[':
                    if brackets > 0:
                        brackets -= 1
                    else:
                        self.cursor = c
                        return

            exit("Fatal Error: Unmatched ']' at position {0}".format(self.cursor))


if __name__ == '__main__':
    bf = Brainfuck()
    #bf.run("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
    bf.run("-,+[-[>>++++[>++++++++<-]<+<-[>+>+>-[>>>]<[[>+<-]>>+>]<<<<<-]]>>>[-]+>--[-[<->[-]]]<[++++++++++++<[>-[>+>>]>[+[<+>-]>+>>]<<<<<-]>>[<+>-]>[-[-<<[-]>>]<<[<<->>-]>>]<<[<<+>>-]]<[-]<.[-]<-,+]")
