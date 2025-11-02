"""
Source file for the BuckLang interpreter. Use the command 

python bucklang.py

to run in interactive mode, or 

python bucklang.py file.buck inputstring

to run the interpreter on the BuckLang file file.buck with
inputstring the initial string written to the tape.
"""

from tapemachine import Tape
from turingmachine import TuringMachine
from bucklang_tools import *
import sys

def interactive_mode() :
    """
    In this mode, the user can interact with a simple tape machine to
    see the output. Only basic tape head commands can be run.
    """

    user_inp = input("Enter a starting string (or type quit).\n")

    interactive_machine = TuringMachine(input_string=user_inp)
    tape = interactive_machine.tape
    usr_command = ""

    while not ("quit" in user_inp or "quit" in usr_command):
        
        print()
        print(interactive_machine)
        
        usr_command = input("> ").strip()
        try :
            if "if" in usr_command :
                # if the usr inputs a standard transition command
                code_tokens = usr_command.split(":")
                code_tokens = {code_tokens[0].replace("if ", "").strip(), code_tokens[1]}

                interactive_machine.run_command(code_tokens=code_tokens)
            else :
                # if the user inputs a tape command
                code_tokens = usr_command.strip().split()
                
                if len(code_tokens) == 2 :
                    if code_tokens == ["move", "left"] :
                        tape.move_left()
                    if code_tokens == ["move", "right"] :
                        tape.move_right()
                    if code_tokens[0] == "write" :
                        tape.write_value(code_tokens[1])
                elif len(code_tokens) == 3 :
                    direction, multiple = code_tokens[1:]
                    if direction == "left" :
                        tape.move_left(multiple=int(multiple))
                    if direction == "right" :
                        tape.move_right(multiple=int(multiple))
        except :
            print("\nInvalid command.\n")

def main(input_file = "", input_word = "", debugging = False) :
    """
    If there is an input buck file, interpret the buck file as a 
    Turing machine and run it from state __top on the input word.

    If there is no input buck file, run in interactive mode.
    """

    # Try to find the given input buck file
    try :
        outputfilename = input_file + "_output.txt"

        # ask the user if they would like the program to track every move of the machine.
        usr_inp = input("Would you like to track the machine's progress? (y/n)\n").strip().lower()
        tracking = (usr_inp[0] == "y")
        
        # Create: 
        # - the index of program lines (called code_lines)
        # - the Turing machine (automatic _machine)
        # Then run the turing machine on the code_lines.
        code_lines = read_code(input_file)
        automatic_machine = TuringMachine(
            input_string = input_word, 
            program = code_lines, 
            tracked=tracking
        )

        with open(outputfilename, "w") as outputfile :
            print("Found", input_file)
            outputfile.write(
                "Running " + input_file 
                    + " on input string " + input_word 
                    + "\nStart Tape:\n"
                    + str(automatic_machine) + "\n(__top)\n"
                )
            
            # If the debugging option is enabled
            if debugging :
                outputfile.write(
                    "States: " + ", ".join(
                        [str(state) for state in automatic_machine.states.keys()]
                        )
                    + "\nProgram:\n\t" + "\n\t".join(
                        [str(code_line) for code_line in automatic_machine.program]
                        )
                        + "\n\n"
                    )
                
        
        # Run the machine
        # print(f"Input tape:\n{automatic_machine}")
        print("\nInput:", input_word)
        result = automatic_machine.run(outputfile=outputfilename)
        output_string = automatic_machine.output()
        # print(f"End tape:\n{result}")
        print("Output:", output_string, "\n")


    except :
        # Something either went wrong with loading the file or no further arguments were given.
        print("-"*40)
        print("Entering interactive mode for a single tape machine. After entering a starting string, run basic tape commands one at a time.")

        interactive_mode()
        
#####################
# Initiates Runtime #
#####################

if __name__ == "__main__" :
    # Collect command line arguments
    system_arguments = sys.argv

    # Clear screen
    print("\n"*100)
    
    # Run main program
    try :
        input_file = system_arguments[1]
    except :
        input_file = None
    
    try : 
        input_word = system_arguments[2]
    except :
        input_word = ""
        
        
    main(input_file = input_file, input_word = input_word, debugging=False)
