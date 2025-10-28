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
    TOPSTATE = "__top"

    def __init__(self, input_string = "", program=["halt"], tracked = False):
        """
        Creates an instance of the Turing Machine.
        Attributes:
            tape            This is the (two-way) tape machine the program is running on.
            program         This is the sequence of 
            tracking        This determines whether the runtime of the machine should be written to an output file.
            states          A dictionary containing all of the state names and where they sit in the program. 
            line_number     The index of the currently running program.
        """
        self.tape = Tape()
        self._tracking = tracked

        # Initialize the tape with the input string
        for c in input_string :
            self.tape.write_value(c)
            self.tape.move_right()

        self.tape.move_left(multiple=len(input_string))

        # Set up the program
        self.program = program

        # In this encoding of a Turing machine, states are the same as "line numbers".
        # This creates a dictionary of what line numbers the states are at. We also 
        # use the state name __top to move the program to the first line.
        self.states = {TuringMachine.TOPSTATE : 0}
        for line_index in range(len(program)) :
            line = program[line_index]
            if len(line) >= 2 and line[0] == TuringMachine.STATE and not (line[1] in self.states.keys()) :
                self.states[line[1]] = line_index

        # Records the current state of the program.
        self.current_state = TuringMachine.TOPSTATE
        
        # Start at the top of the program and scan downwards.
        self.line_number = 0

    def run_command(self, code_tokens, outputfile=None) :
        """
        Runs a single line of the program.
        """
        
        # input(code_tokens)    # for debugging
        
        # If the code_tokens are a list, then they must be the keyword state and a state name
        if type(code_tokens) == list :
            statename = code_tokens[1]
            self.current_state = statename

        # If the code_tokes are a dictionary, then they correspond to a line of the program
        if type(code_tokens) == dict :

            # Get the symbol under the tape head
            reading = self.tape.read_value()

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
                            self.tape.move_left(multiple=aux_argument)
                        else :
                            self.tape.move_left()

                    if command == TuringMachine.MOVE and argument[0] == "r" :
                        if aux_argument != None :
                            self.tape.move_right(multiple=aux_argument)
                        else :
                            self.tape.move_right()

                    if command == TuringMachine.WRITE :
                        self.tape.write_value(str(argument))

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
            # if self._tracking :
            #     print(self, "\n")

            code_tokens = self.program[self.line_number]
            self.run_command(code_tokens=code_tokens, outputfile=outputfile)

        return str(self)


    def __str__(self):
        return str(self.tape)
    