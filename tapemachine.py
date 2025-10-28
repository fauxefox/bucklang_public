class Tape :
    """
    A class that denotes a tape machine.

    Attributes:
    # 
        _tape_list          The data stored on the tape.
        _tape_head          The index at which the tape head appears in tape_list. 
                            Informally, the position of the tape head.
        _tape_length        Current amount of tape rendered. _tape_list expands when trying to move the tape head out of bounds.
    """

    # Directions
    RIGHT = "right"
    LEFT = "left"
    BLANK = "_"

    def __init__(self, start_values = [ BLANK ]):
        """
        Creates an instance of a tape machine.
        """
        self._tape_list = []
        self._tape_head = 0


        self._tape_length = len(start_values)

        for value in start_values :
            self._tape_list.append(str(value))

    def _extend_tape(self, direction) :
        """
        Increase the span of tape cells reached by the tape head.
        Direction denotes which end of the tape needs expanding.
        """
        if direction == Tape.RIGHT :
            self._tape_list.append(Tape.BLANK)

        if direction == Tape.LEFT :
            self._tape_list = [Tape.BLANK] + self._tape_list
    
        # Increase width of used tape by 1
        self._tape_length += 1

    def move_right(self, multiple = 1, enroute = False) :
        """
        Move the tape head to the right. 
        If multiple steps are indicated, "enroute" might be used to prevent every step being printed/written to the output file.
        """
        for _ in range(multiple) :
            if self._tape_head >= self._tape_length - 1 :
                self._extend_tape(Tape.RIGHT)
            
            # move the tape head to the right
            self._tape_head += 1

    def move_left(self, multiple = 1, enroute = False) :
        """
        Move the tape head to the left. 
        If multiple steps are indicated, "enroute" might be used to prevent every step being printed/written to the output file.
        """
        for _ in range(multiple) :
            if self._tape_head == 0 :
                # just expanding to the left simulates moving the tape head left
                self._extend_tape(Tape.LEFT)
            else : 
                # If there is room to the left, move the tape head left
                self._tape_head -= 1
            
    def read_value(self) :
        """
        Returns the symbol under the tape head.
        """
        return self._tape_list[self._tape_head]
    
    def write_value(self, value) :
        """
        Writes the symbol `value` to the tape under the tape head.
        """
        self._tape_list[self._tape_head] = str(value)

    def erase_value(self) :
        """
        Writes a blank under the tape head.
        """
        self.write_value(Tape.BLANK)

    def _get_list_position (self) :
        """
        Get position of the tape head in the list representation.
        """
        return self._tape_head
    
    def move_to(self, line) :
        """
        Cheater function! Moves the head to a particular index on the list representation.
        """
        while line > self._tape_head :
            self.move_right(enroute = True)

        while line < self._tape_head :
            self.move_left(enroute = True)

    def __str__(self):
        """
        Returns a string representation of the tape.
        """
        str_rep = "... "
        str_hed = "    " 
        for line in range(self._tape_length) :
            value = self._tape_list[line]
            value_len = len(value)

            str_rep += f"{value} | "


            if self._tape_head == line :
                str_hed += f"V{" "*(value_len - 1)}"
            else :
                str_hed += f"{" "*(value_len + 3)}"
        
        return f"{str_hed}\n{str_rep} ..."