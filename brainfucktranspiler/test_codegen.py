from .codegen import (
    TapeStack,
    op_add,
    op_copy,
    op_input,
    op_output,
    op_multiply,
    op_minus,
    op_not,
)
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


def test_minus_io() -> None:
    tape = TapeStack()
    result = tape.register_variable("result")
    left = tape.register_variable("left")
    right = tape.register_variable("right")
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_minus(tape, result, left, right)
        + op_output(tape, result)
    )

    sm = StateMachine(code, [7, 5])
    assert sm.run() == [2]


def test_not_io() -> None:
    tape = TapeStack()
    var = tape.register_variable("var")
    code = op_input(tape, var) + op_not(tape, var) + op_output(tape, var)
    print(code)

    sm = StateMachine(code, [2])
    assert sm.run() == [0]
    sm = StateMachine(code, [1])
    assert sm.run() == [0]
    sm = StateMachine(code, [0])
    assert sm.run() == [1]
