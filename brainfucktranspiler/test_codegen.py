from .codegen import (
    TapeStack,
    op_add,
    op_copy,
    op_input,
    op_output,
    op_multiply,
    op_minus,
    op_not,
    op_less,
    op_and,
    op_subtract_smaller,
    op_less_equals,
)
from .interpreter import StateMachine


def test_copy() -> None:
    tape = TapeStack()
    source = tape.register_variable()
    destination = tape.register_variable()
    code = (
        op_input(tape, source)
        + op_copy(tape, destination, source)
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
        + op_add(tape, result, left, right)
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
        + op_multiply(tape, result, left, right)
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
        + op_minus(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [7, 5]).run() == [2]


def test_not() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    condition = tape.register_variable()
    code = (
        op_input(tape, condition)
        + op_not(tape, result, condition)
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
        + op_and(tape, result, left, right)
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
    assert StateMachine(code, [2, 4]).run() == [0, 2]
    assert StateMachine(code, [2, 1]).run() == [1, 0]
    assert StateMachine(code, [1, 1]).run() == [0, 0]
    assert StateMachine(code, [0, 0]).run() == [0, 0]


def test_less() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_less(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 2]).run() == [0]
    assert StateMachine(code, [1, 2]).run() == [1]
    assert StateMachine(code, [2, 1]).run() == [0]


def test_less_equals() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    left = tape.register_variable()
    right = tape.register_variable()
    code = (
        op_input(tape, left)
        + op_input(tape, right)
        + op_less_equals(tape, result, left, right)
        + op_output(tape, result)
    )
    assert StateMachine(code, [2, 2]).run() == [1]
    assert StateMachine(code, [1, 2]).run() == [1]
    assert StateMachine(code, [2, 1]).run() == [0]
