import string

def read_code(filename : str) :
    """
    Given a filename, this reads in the code line by line and creates a list of commands.
    """
    code_lines = []
    with open(filename, "r") as file :
        file_lines = file.readlines()
        
        for line in file_lines :
            # ignore case, strip whitespace
            new_line = line.lstrip().rstrip()

            # if a command, split by spaces and append to code_lines
            if len(new_line) > 0 and new_line[0] != "#" :
                if ":" in new_line :
                    condition, commands = new_line.split(":")
                    condition = condition[3:].strip()
                    laundry_list = commands.split(".")
                    laundry_list = [
                        command.strip() for command in laundry_list
                        ]
                    code_line = {condition : laundry_list}

                else : 
                    code_line = new_line.strip().split()

                code_lines.append(code_line)

    return code_lines

def string_clean(unclean : str) :
    """
    Totally cleans a string representation of something.
    """
    for c in string.whitespace :
        unclean = unclean.replace(c, "")
    
    return unclean.lower()
