from tapemachine import Tape
from bucklang_tools import *


class TuringMachine :
    """
    A class that captures our notion of Turing machine.
    """

    MOVE = "move"
    WRITE = "write"
    GOTO = "goto"
    STATE = "state"

    def __init__(self, input_string = "", program=["halt"], tracked = False):
        
        self.tape = Tape()
        self._tracking = tracked

        # Initialize the tape with the input string
        for c in input_string :
            self.tape.write_value(c)
            self.tape.move_right()

        self.tape.move_left(multiple=len(input_string))

        # Set up the program
        self.program = program

        # In this encoding of a Turing machine, states are the same as "line numbers"
        self.line_number = 0

        # But we can still carry a dictionary of "what line numbers the states are at"
        self.states = {"init" : 0}
        for line_index in range(len(program)) :
            line = program[line_index]
            if len(line) >= 2 and line[0] == TuringMachine.STATE and not (line[1] in self.states.keys()) :
                self.states[line[1]] = line_index

    def run_command(self, code_tokens, outputfile=None) :
        tape = self.tape


        if type(code_tokens) == list :
            statename = code_tokens[1]
            self.line_number = self.states[statename]
        
        if type(code_tokens) == dict :
            reading = self.tape.read_value()
            # input(code_tokens)

            if reading in code_tokens.keys() :
                laundry_list = code_tokens[reading]

                for item in laundry_list :
                    command_tokens = item.split()
                    command = command_tokens[0]
                    
                    try :
                        argument = command_tokens[1]
                    except :
                        argument = None
                    
                    try :
                        aux_argument = command_tokens[2]
                    except :
                        aux_argument = None

                    if command == TuringMachine.MOVE and argument[0] == "l" :
                        if aux_argument != None :
                            tape.move_left(multiple=aux_argument)
                        else :
                            tape.move_left()

                    if command == TuringMachine.MOVE and argument[0] == "r" :
                        if aux_argument != None :
                            tape.move_right(multiple=aux_argument)
                        else :
                            tape.move_right()

                    if command == TuringMachine.WRITE :
                        tape.write_value(str(argument))

                    if command == TuringMachine.GOTO and argument in self.states.keys() :
                        self.line_number = self.states[argument]
                        return
                    

                    # if there is a specified output file, write to it
                    if outputfile != None and self._tracking :
                        with open(outputfile, "a") as output :
                            
                            output.write(f"{self}\n{item}\n\n")
    
        self.line_number += 1
        return
            
    def run(self, outputfile = None) :
        """
        Runs the Turing machine on the provided tape and the provided program.
        """

        # While we are on a line that corresponds to a command, run the program
        while self.line_number >= 0 and self.line_number < len(self.program) :
            if self._tracking :
                print(self, "\n")

            code_tokens = self.program[self.line_number]
            self.run_command(code_tokens=code_tokens, outputfile=outputfile)


    def __str__(self):
        return str(self.tape)