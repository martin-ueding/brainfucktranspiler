from .codegen import TapeStack, op_add, op_copy, op_input, op_output, op_multiply
from .interpreter import StateMachine


def test_op_add() -> None:
    tape = TapeStack()
    result = tape.register_variable("result")
    left = tape.register_variable("left")
    right = tape.register_variable("right")
    code = op_add(tape, result, left, right)
    assert code == ">[-<+>]>[-<<+>>]"


def test_op_copy() -> None:
    tape = TapeStack()
    source = tape.register_variable("source")
    destination = tape.register_variable("destination")
    code = op_copy(tape, destination, source)
    assert code == ">>[-]<<[->+>+<<]>>[-<<+>>]"


def test_op_add_io() -> None:
    tape = TapeStack()
    result = tape.register_variable("result")
    left = tape.register_variable("left")
    right = tape.register_variable("right")
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_add(tape, result, left, right)
        + op_output(tape, result)
    )

    sm = StateMachine(code, [2, 3])
    assert sm.run() == [5]


def test_multiply_io() -> None:
    tape = TapeStack()
    result = tape.register_variable("result")
    left = tape.register_variable("left")
    right = tape.register_variable("right")
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_multiply(tape, result, left, right)
        + op_output(tape, result)
    )

    sm = StateMachine(code, [2, 3])
    assert sm.run() == [6]
