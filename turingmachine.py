from tapemachine import Tape
from bucklang_tools import *


class TuringMachine :
    """
    A class that captures our notion of Turing machine.
    """

    MOVE = "move"
    WRITE = "write"
    GOTO = "goto"
    ERASE = "erase"
    STATE = "state"
    TOPSTATE = "__top"
    HALT = "halt"

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

        self._clocktime = 0

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
            if (
                len(line) >= 2 
                and line[0] == TuringMachine.STATE 
            ) :
                statename = line[1]
                self.states[statename] = line_index

        # Make sure they set a top state!
        # assert self.states[TuringMachine.TOPSTATE] > -1

        # Records the current state of the program
        self.current_state = TuringMachine.TOPSTATE
        
        # Start at the top of the program and scan downwards.
        self.line_number = self.states[self.current_state]

    def run_command(self, code_tokens, outputfile=None) :
        """
        Runs a single line of the program.
        """

        # increase time
        self._clocktime += 1
        
        # If the code_tokens are a list, then they must be the keyword state and a state name
        if type(code_tokens) == list :
            statename = code_tokens[1]
            self.current_state = statename

        # If the code_tokes are a dictionary, then they correspond to a line of the program
        elif type(code_tokens) == dict :

            # Get the symbol under the tape head
            reading = string_clean(self.tape.read_value())
            
            # If currently reading the conditional guard, run proceeding program.     
            # input(reading + " sat condition " + ", ".join(code_tokens.keys()) + str(reading in code_tokens.keys()))  
            if reading in code_tokens.keys() :

                # Gather the "laundry list" of tape machine commands and run in order
                laundry_list = code_tokens[reading]

                for item in laundry_list :
                    # each item in the laundry list is a string of the form
                    #   "command argument (aux argument)"
                    item : str          

                    command_tokens = item.split()
                    command = command_tokens[0]
                    

                    # Try to find an argument (not every command has one)
                    try :
                        argument = command_tokens[1]
                    except :
                        argument = None
                    

                    # Try to find a second (aux) argument
                    try :
                        aux_argument = command_tokens[2]
                    except :
                        aux_argument = None

                    ##########
                    ##### THIS IS AN EXCELLENT PLACE TO DEBUG
                    debugging = False
                    if debugging :
                        input(" ".join(
                            [
                                "state " + self.current_state, 
                                str(code_tokens.keys()),
                                str(reading),
                                str(command), 
                                str(argument), 
                                str(aux_argument)
                            ]
                            )
                        )
                    ###########################################

                    # Now go through the possible commands one at a time
                    if command == TuringMachine.MOVE and argument[0] == "l" :

                        if aux_argument != None :
                            # Here, move got a "multiples" argument
                            self.tape.move_left(multiple = aux_argument)
                        else :
                            self.tape.move_left()

                    elif command == TuringMachine.MOVE and argument[0] == "r" :
                        
                        if aux_argument != None :
                            # Here, move got a "multiples" argument
                            self.tape.move_right(multiple=aux_argument)
                        else :
                            self.tape.move_right()

                    elif command == TuringMachine.WRITE :
                        self.tape.write_value(str(argument))

                    elif command == TuringMachine.ERASE :
                        self.tape.write_value(Tape.BLANK)

                    elif command == TuringMachine.GOTO and argument in self.states.keys() :
                        self.line_number = self.states[argument]

                        # In this case, we are changing states, so we do not increment the line number
                        return "transition to state " + str(argument)

                    elif command == TuringMachine.HALT : 
                        return "eop"

                    # if there is a specified output file and we are tracking, write to it
                    if outputfile != None and self._tracking :
                        with open(outputfile, "a") as output :
                            
                            output.write(
                                str(self) \
                                    + "\n (" + str(self.current_state) 
                                    + ") " + str(item) + " \n"
                                )
        
        # input(" ".join([self.current_state, self.tape.read_value()]))

        if (
            (len(self.program) <= self.line_number + 1)
            or (type(self.program[self.line_number + 1]) == list)
        ) :
            return "eop"
        else :        
            self.line_number += 1
    
            
    def run(self, outputfile = None) :
        """
        Runs the Turing machine on the provided tape and the provided program.
        """

        # While we are on a line that corresponds to a command, run the program
        while self.line_number >= 0 and self.line_number < len(self.program) :
            code_tokens = self.program[self.line_number]
            result = self.run_command(code_tokens=code_tokens, outputfile=outputfile)

            if result == "eop" :
                break
        

    def get_clock(self) :
        return self._clocktime

    def __str__(self):
        return str(self.tape)
    
    def output(self) -> str : 
        output_str = ""
        for cell in self.tape._tape_list : 
            if str(cell) != "_" : 
                output_str += str(cell)
        
        return output_str
    