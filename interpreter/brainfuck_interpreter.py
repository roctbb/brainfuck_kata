from enum import Enum


class NoInputException(Exception):
    pass


class NoOutputException(Exception):
    pass


class IncorrectCodeException(Exception):
    pass


class LiteralTypes(Enum):
    POINTER_RIGHT = 1
    POINTER_LEFT = 2
    INC = 3
    DEC = 4
    PRINT_ONE = 5
    INPUT_ONE = 6
    START_LOOP = 7
    END_LOOP = 8


class BrainfuckInterpreter:
    MEMORY_SIZE = 30000
    CELL_SIZE = 256

    LITERALS = {
        ">": LiteralTypes.POINTER_RIGHT,
        "<": LiteralTypes.POINTER_LEFT,
        "+": LiteralTypes.INC,
        "-": LiteralTypes.DEC,
        ".": LiteralTypes.PRINT_ONE,
        ",": LiteralTypes.INPUT_ONE,
        "[": LiteralTypes.START_LOOP,
        "]": LiteralTypes.END_LOOP
    }

    def __init__(self):

        self._literal_methods = {
            LiteralTypes.POINTER_RIGHT: self._increase_pointer,
            LiteralTypes.POINTER_LEFT: self._decrease_pointer,
            LiteralTypes.INC: self._increase_value,
            LiteralTypes.DEC: self._decrease_value,
            LiteralTypes.PRINT_ONE: self._print_value,
            LiteralTypes.INPUT_ONE: self._read_value,
            LiteralTypes.START_LOOP: self._start_loop,
            LiteralTypes.END_LOOP: self._end_loop,
        }

        self._create_initial_state()

    def clear(self):
        self._create_initial_state()

    def _create_initial_state(self):
        self._memory_pointer = 0
        self._code_pointer = 0
        self._memory = [0 for _ in range(self.MEMORY_SIZE)]
        self._input = []
        self._output = []
        self._program = []

    def give_input(self, string):
        self._input += list(string)

    def get_output(self):
        if self._output:
            result = ''.join(self._output)
            self._output = []
            return result
        else:
            raise NoOutputException

    def run(self, program: str):
        self._load_program(program)
        self._check_program()
        self._execute_program()

    def _load_program(self, program: str):
        self._program = list(program)
        self._code_pointer = 0

    def _check_program(self):
        if not self._program_correct():
            raise IncorrectCodeException

    def _execute_program(self):
        while self._program_not_ended():
            current_literal_type = self._get_current_literal_type()
            self._run_literal_method(current_literal_type)

    def _run_literal_method(self, literal):
        self._literal_methods[literal]()

    def _get_current_literal(self):
        return self._get_literal_for_position(self._code_pointer)

    def _get_current_literal_type(self):
        return self._get_literal_type_for_position(self._code_pointer)

    def _get_literal_type_for_position(self, pos):
        return self.LITERALS[self._get_literal_for_position(pos)]

    def _get_literal_for_position(self, pos):
        return self._program[pos]

    def _program_not_ended(self):
        return self._code_pointer < len(self._program)

    def _program_correct(self):
        if self._have_inconsistent_brakets() or self._have_unknown_literals():
            return False
        return True

    def _have_inconsistent_brakets(self):
        loop_start_literal = self._find_literal_for_type(LiteralTypes.START_LOOP)
        loop_end_literal = self._find_literal_for_type(LiteralTypes.END_LOOP)
        return self._program.count(loop_start_literal) != self._program.count(loop_end_literal)

    def _find_literal_for_type(self, literal_type):
        type_to_literal = {v: k for k, v in self.LITERALS.items()}
        return type_to_literal[literal_type]

    def _have_unknown_literals(self):
        return len([literal for literal in self._program if literal not in self.LITERALS]) > 0

    def _increase_pointer(self):
        self._memory_pointer += 1
        self._memory_pointer %= self.MEMORY_SIZE
        self._code_pointer += 1

    def _decrease_pointer(self):
        self._memory_pointer -= 1
        self._memory_pointer %= self.MEMORY_SIZE
        self._code_pointer += 1

    def _increase_value(self):
        self._memory[self._memory_pointer] += 1
        self._memory[self._memory_pointer] %= self.CELL_SIZE
        self._code_pointer += 1

    def _decrease_value(self):
        self._memory[self._memory_pointer] -= 1
        self._memory[self._memory_pointer] %= self.CELL_SIZE
        self._code_pointer += 1

    def _print_value(self):
        symbol = chr(self._memory[self._memory_pointer])
        self._output.append(symbol)
        self._code_pointer += 1

    def _read_value(self):
        if self._input:
            self._memory[self._memory_pointer] = ord(self._input[0])
            del self._input[0]
            self._code_pointer += 1
        else:
            raise NoInputException

    def _start_loop(self):
        if self._memory[self._memory_pointer] != 0:
            self._code_pointer += 1
        else:
            self._code_pointer = self._find_right_paired_bracket() + 1

    def _end_loop(self):
        if self._memory[self._memory_pointer] == 0:
            self._code_pointer += 1
        else:
            self._code_pointer = self._find_left_paired_bracket() + 1

    def _find_right_paired_bracket(self):
        return self._find_bracket(LiteralTypes.START_LOOP, LiteralTypes.END_LOOP, -1)

    def _find_left_paired_bracket(self):
        return self._find_bracket(LiteralTypes.END_LOOP, LiteralTypes.START_LOOP, -1)

    def _find_bracket(self, left, right, step):
        level = 0
        position = self._code_pointer + step

        while position < len(self._program):
            literal_type = self._get_literal_type_for_position(position)

            if literal_type == left:
                level += 1

            if literal_type == right:
                if level == 0:
                    return position
                else:
                    level -= 1

            position += step
