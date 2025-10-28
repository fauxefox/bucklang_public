from tapemachine import Tape
from turingmachine import TuringMachine
from bucklang_tools import *
import sys
import io


def interactive_mode() :
    print("-"*40)
    print("Entering interactive mode for a single tape machine. After entering a starting string, run commands one at a time.")
    user_inp = input("Enter a starting string.\n")

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

def main(input_file = "", input_word = "") :
    try :
        outputfilename = input_file + "_output.txt"
        with open(outputfilename, "w") as outputfile :
            print("Found", input_file)
            outputfile.write("Running " + input_file + "\n\n")


        usr_inp = input("Would you like to track the machine's progress? (y/n)\n").strip().lower()
        tracking = (usr_inp[0] == "y")
        
        code_lines = read_code(input_file)
        automatic_machine = TuringMachine(input_string = input_word, program = code_lines, tracked=tracking)
        print(f"Input tape:\n{automatic_machine}")
        result = automatic_machine.run(outputfile=outputfilename)
        print(f"Output tape:\n{result}")
    except :
        interactive_mode()
        


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
        
        
    main(input_file = input_file, input_word = input_word)
