import sys
import io

def read_code(filename) :
    """
    Given a filename, this reads in the code line by line and creates a list of commands.
    """
    code_lines = []
    with open(filename, "r") as file :
        file_lines = file.readlines()
        
        for line in file_lines :
            # ignore case, strip whitespace
            new_line = line.lower().strip()

            # if a command, split by spaces and append to code_lines
            if len(new_line) > 0 and new_line[0] != "#" :
                if ":" in new_line :
                    condition, commands = new_line.split(":")
                    condition = condition.replace("if ", "").replace(" ", "")
                    code_line = {condition : commands.split(".")}
                else : 
                    code_line = new_line.split()

                code_lines.append(code_line)

    # print(code_lines)
    return code_lines


