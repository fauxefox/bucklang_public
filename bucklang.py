from tapemachine import Tape
from turingmachine import TuringMachine
from bucklang_tools import *
import sys
import io


def interactive_mode() :
    print("-"*40)
    print("Entering interactive mode. After entering a starting string, run commands one at a time.")
    user_inp = input("Enter a starting string.\n")

    interactive_machine = TuringMachine(input_string=user_inp)
    command = ""

    while not ("quit" in user_inp or "quit" in command):
        
        print()
        print(interactive_machine)
        
        command = input("> ")
        code_tokens = command.strip().split()
        interactive_machine.run_command(code_tokens=code_tokens)

def main(input_file = "", input_word = "") :
    outputfilename = input_file + "_output.txt"
    try :
        with open(outputfilename, "w") as outputfile :
            print("Found", input_file)
            outputfile.write("Running " + input_file + "\n\n")


        usr_inp = input("Would you like to track the machine's progress? (y/n)\n").strip().lower()
        tracking = (usr_inp[0] == "y")
        
        code_lines = read_code(input_file)
        automatic_machine = TuringMachine(input_string = input_word, program = code_lines, tracked=tracking)
        automatic_machine.run(outputfile=outputfilename)

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
