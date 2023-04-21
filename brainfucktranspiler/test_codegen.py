from .codegen import (
    TapeStack,
    fn_plus,
    fn_copy,
    op_input,
    op_output,
    fn_multiply,
    fn_minus,
    fn_not,
    fn_less,
    fn_and,
    op_subtract_smaller,
    fn_less_equals,
    fn_divide,
)
from .interpreter import StateMachine


def test_copy() -> None:
    tape = TapeStack()
    source = tape.register_variable()
    destination = tape.register_variable()
    code = (
        op_input(tape, source)
        + fn_copy(tape, destination, source)
        + op_output(tape, destination)
    )
    assert StateMachine(code, [2]).run() == [2]


def test_add() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_plus(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 3]).run() == [5]


def test_multiply() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_multiply(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 3]).run() == [6]


def test_minus() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_minus(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [7, 5]).run() == [2]


def test_minus_inplace_left() -> None:
    tape = TapeStack()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_minus(tape, left, left, right)
        + op_output(tape, left)
    )
    assert StateMachine(code, [7, 5]).run() == [2]


def test_minus_inplace_right() -> None:
    tape = TapeStack()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_minus(tape, right, left, right)
        + op_output(tape, right)
    )
    assert StateMachine(code, [7, 5]).run() == [2]


def test_not() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    condition = tape.register_variable()
    code = (
        op_input(tape, condition)
        + fn_not(tape, result, condition)
        + op_output(tape, result)
    )
    assert StateMachine(code, [0]).run() == [1]
    assert StateMachine(code, [1]).run() == [0]
    assert StateMachine(code, [2]).run() == [0]


def test_and() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_and(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [0, 0]).run() == [0]
    assert StateMachine(code, [0, 1]).run() == [0]
    assert StateMachine(code, [1, 0]).run() == [0]
    assert StateMachine(code, [1, 1]).run() == [1]


def test_subtract_smaller() -> None:
    tape = TapeStack()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_subtract_smaller(tape, left, right)
        + op_output(tape, left)
        + op_output(tape, right)
    )
    assert StateMachine(code, [2, 5]).run() == [0, 3]
    assert StateMachine(code, [5, 2]).run() == [3, 0]
    assert StateMachine(code, [3, 3]).run() == [0, 0]
    assert StateMachine(code, [0, 0]).run() == [0, 0]
    assert StateMachine(code, [15, 10]).run() == [5, 0]
    assert StateMachine(code, [10, 15]).run() == [0, 5]


def test_less() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_less(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 2]).run() == [0]
    assert StateMachine(code, [1, 2]).run() == [1]
    assert StateMachine(code, [2, 1]).run() == [0]
    assert StateMachine(code, [10, 15]).run() == [1]
    assert StateMachine(code, [10, 10]).run() == [0]
    assert StateMachine(code, [15, 10]).run() == [0]


def test_less_equals() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + fn_less_equals(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 2]).run() == [1]
    assert StateMachine(code, [1, 2]).run() == [1]
    assert StateMachine(code, [2, 1]).run() == [0]
    assert StateMachine(code, [10, 15]).run() == [1]
    assert StateMachine(code, [10, 10]).run() == [1]
    assert StateMachine(code, [15, 10]).run() == [0]


def test_divide() -> None:
    tape = TapeStack()
    quotient = tape.register_variable()
    remainder = tape.register_variable()
    dividend = tape.register_variable()
    divisor = tape.register_variable()
    code = (
        op_input(tape, dividend)
        + op_input(tape, divisor)
        + fn_divide(tape, quotient, remainder, dividend, divisor)
        + op_output(tape, quotient)
        + op_output(tape, remainder)
    )
    assert StateMachine(code, [0, 1]).run() == [0, 0]
    assert StateMachine(code, [1, 1]).run() == [1, 0]
    assert StateMachine(code, [2, 1]).run() == [2, 0]
    assert StateMachine(code, [1, 2]).run() == [0, 1]
    assert StateMachine(code, [10, 3]).run() == [3, 1]
    assert StateMachine(code, [10, 5]).run() == [2, 0]
