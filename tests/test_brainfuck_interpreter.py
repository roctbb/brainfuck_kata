import pytest

from interpreter import BrainfuckInterpreter, NoOutputException, NoInputException, IncorrectCodeException


def test_initial_state():
    interpreter = BrainfuckInterpreter()

    assert interpreter._memory_pointer == 0
    assert len(interpreter._memory) == interpreter.MEMORY_SIZE

    for cell in interpreter._memory:
        assert cell == 0

    with pytest.raises(NoOutputException):
        interpreter.get_output()
    assert interpreter._input == []


def test_rarrow_moves_pointer():
    interpreter = BrainfuckInterpreter()

    interpreter.run('>')

    assert interpreter._memory_pointer == 1


def test_multiple_rarrow_moves_pointer():
    interpreter = BrainfuckInterpreter()

    interpreter.run('>>>')

    assert interpreter._memory_pointer == 3


def test_sequental_rarrow_moves_pointer():
    interpreter = BrainfuckInterpreter()

    interpreter.run('>')
    assert interpreter._memory_pointer == 1

    interpreter.run('>')
    assert interpreter._memory_pointer == 2


def test_larrow_moves_pointer():
    interpreter = BrainfuckInterpreter()
    interpreter._memory_pointer = 1

    interpreter.run('<')

    assert interpreter._memory_pointer == 0


def test_arrows_corner_conditions():
    interpreter = BrainfuckInterpreter()

    interpreter.run('<')
    assert interpreter._memory_pointer == interpreter.MEMORY_SIZE - 1

    interpreter.run('>')
    assert interpreter._memory_pointer == 0


def test_increment_and_decrement():
    interpreter = BrainfuckInterpreter()

    interpreter.run('+')
    assert interpreter._memory[interpreter._memory_pointer] == 1

    interpreter.run('-')
    assert interpreter._memory[interpreter._memory_pointer] == 0


def test_increment_and_decrement_corner_conditions():
    interpreter = BrainfuckInterpreter()

    interpreter.run('-')
    assert interpreter._memory[interpreter._memory_pointer] == interpreter.CELL_SIZE - 1

    interpreter.run('+')
    assert interpreter._memory[interpreter._memory_pointer] == 0


def test_give_input():
    interpreter = BrainfuckInterpreter()

    interpreter.give_input("ab")
    interpreter.give_input("c")

    assert interpreter._input == ['a', 'b', 'c']


def test_correct_output():
    interpreter = BrainfuckInterpreter()

    interpreter.run('+' * 33 + '..')

    assert interpreter.get_output() == chr(33) + chr(33)

    with pytest.raises(NoOutputException):
        interpreter.get_output()


def test_correct_input():
    interpreter = BrainfuckInterpreter()

    interpreter.give_input("abc")

    interpreter.run(',.' * 3)

    assert interpreter.get_output() == "abc"


def test_input_from_empty_buffer():
    interpreter = BrainfuckInterpreter()

    with pytest.raises(NoInputException):
        interpreter.run(',')


def test_get_output_from_empty_buffer():
    interpreter = BrainfuckInterpreter()

    with pytest.raises(NoOutputException):
        interpreter.get_output()


def test_raises_exception_on_incorrect_literals():
    interpreter = BrainfuckInterpreter()

    with pytest.raises(IncorrectCodeException):
        interpreter.run(">>>>abc")


def test_raises_exception_on_incosistent_brakets():
    interpreter = BrainfuckInterpreter()

    with pytest.raises(IncorrectCodeException):
        interpreter.run(">>[[>>]>")

    with pytest.raises(IncorrectCodeException):
        interpreter.run(">>[")

    with pytest.raises(IncorrectCodeException):
        interpreter.run(">>]>")


def test_negative_condition():
    interpreter = BrainfuckInterpreter()

    interpreter.run('[+>]<++.')
    assert interpreter.get_output() == chr(2)


def test_positive_condition():
    interpreter = BrainfuckInterpreter()

    interpreter.run('+[+>]<++.')
    assert interpreter.get_output() == chr(4)

def test_loop():
    interpreter = BrainfuckInterpreter()

    interpreter.run('++++[.-]+.')
    assert interpreter.get_output() == chr(4) + chr(3) + chr(2) + chr(1) + chr(1)

def test_hello_world():
    interpreter = BrainfuckInterpreter()

    interpreter.run(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<++++++++>-]<-.--------.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.")

    assert interpreter.get_output() == "Hello world!\n"

def test_clear():
    interpreter = BrainfuckInterpreter()

    interpreter.run('+')

    interpreter.clear()

    interpreter.run('.')
    assert interpreter.get_output() == chr(0)