import abc
from typing import Callable


class Variable:
    def __init__(self, position: int) -> None:
        self.position = position


class TapeStack:
    def __init__(self) -> None:
        self._stack = []
        self._position = 0

    def register_variable(self) -> Variable:
        new_position = len(self._stack)
        new_variable = Variable(new_position)
        self._stack.append(new_variable)
        return new_variable

    def unregister_variable(self, variable: Variable) -> None:
        assert self._stack[-1] == variable
        self._stack.pop()

    def seek(self, variable: Variable) -> str:
        result = []
        while variable.position > self._position:
            result.append(">")
            self._position += 1
        while variable.position < self._position:
            result.append("<")
            self._position -= 1
        return "".join(result)


def op_decrement(tape: TapeStack, var: Variable) -> str:
    return tape.seek(var) + "-"


def op_increment(tape: TapeStack, var: Variable) -> str:
    return tape.seek(var) + "+"


def op_input(tape: TapeStack, var: Variable) -> str:
    return tape.seek(var) + ","


def op_output(tape: TapeStack, var: Variable) -> str:
    return tape.seek(var) + "."


def op_while(tape, condition: Variable, body: Callable[[], str]) -> str:
    return tape.seek(condition) + "[" + body() + tape.seek(condition) + "]"


def op_clear(tape: TapeStack, var: Variable) -> str:
    return op_while(tape, var, lambda: op_decrement(tape, var))


def op_if(tape, condition: Variable, body: Callable[[], str]) -> str:
    return op_while(tape, condition, lambda: body() + op_clear(tape, condition))


def op_accumulate(tape: TapeStack, accumulator: Variable, summand: Variable) -> str:
    return op_while(
        tape,
        summand,
        lambda: (op_decrement(tape, summand) + op_increment(tape, accumulator)),
    )


def op_subtract(tape: TapeStack, accumulator: Variable, summand: Variable) -> str:
    return op_while(
        tape,
        summand,
        lambda: (op_decrement(tape, summand) + op_decrement(tape, accumulator)),
    )


def fn_copy(tape: TapeStack, destination: Variable, source: Variable) -> str:
    temp = tape.register_variable()
    code = (
        op_clear(tape, temp)
        + op_clear(tape, destination)
        + op_while(
            tape,
            source,
            lambda: (
                op_decrement(tape, source)
                + op_increment(tape, destination)
                + op_increment(tape, temp)
            ),
        )
        + op_accumulate(tape, source, temp)
    )
    tape.unregister_variable(temp)
    return code


def fn_plus(tape: TapeStack, result: Variable, left: Variable, right: Variable) -> str:
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, result)
        + op_accumulate(tape, result, left_copy)
        + op_accumulate(tape, result, right_copy)
    )
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    return code


def fn_minus(tape: TapeStack, result: Variable, left: Variable, right: Variable) -> str:
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, result)
        + op_accumulate(tape, result, left_copy)
        + op_subtract(tape, result, right_copy)
    )
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    return code


def fn_multiply(
    tape: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    temp = tape.register_variable()
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, temp)
        + op_while(
            tape,
            left_copy,
            lambda: (
                op_decrement(tape, left_copy)
                + fn_copy(tape, temp, right_copy)
                + op_accumulate(tape, result, temp)
            ),
        )
    )
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    tape.unregister_variable(temp)
    return code


def fn_not(tape: TapeStack, result: Variable, condition: Variable) -> str:
    condition_copy = tape.register_variable()
    code = (
        fn_copy(tape, condition_copy, condition)
        + op_clear(tape, result)
        + op_increment(tape, result)
        + op_if(tape, condition_copy, lambda: op_clear(tape, result))
    )
    tape.unregister_variable(condition_copy)
    return code


def fn_and(tape: TapeStack, result: Variable, left: Variable, right: Variable) -> str:
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, result)
        + op_if(
            tape,
            left_copy,
            lambda: op_if(tape, right_copy, lambda: op_increment(tape, result)),
        )
    )
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    return code


def op_subtract_smaller(tape: TapeStack, left: Variable, right: Variable) -> str:
    temp_and = tape.register_variable()
    cond = lambda: fn_and(tape, temp_and, left, right)
    code = cond() + op_while(
        tape,
        temp_and,
        lambda: (op_decrement(tape, left) + op_decrement(tape, right) + cond()),
    )
    tape.unregister_variable(temp_and)
    return code


def fn_less(tape: TapeStack, result: Variable, left: Variable, right: Variable) -> str:
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    not_left = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, result)
        + op_subtract_smaller(tape, left_copy, right_copy)
        + fn_not(tape, not_left, left_copy)
        + fn_and(tape, result, not_left, right_copy)
    )
    tape.unregister_variable(not_left)
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    return code


def fn_less_equals(
    tape: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    left_copy = tape.register_variable()
    right_copy = tape.register_variable()
    code = (
        fn_copy(tape, left_copy, left)
        + fn_copy(tape, right_copy, right)
        + op_clear(tape, result)
        + op_subtract_smaller(tape, left_copy, right_copy)
        + fn_not(tape, result, left_copy)
    )
    tape.unregister_variable(right_copy)
    tape.unregister_variable(left_copy)
    return code


def fn_greater(
    tape: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    return fn_less(tape, result, right, left)


def fn_greater_equals(
    tape: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    return fn_less_equals(tape, result, right, left)


def fn_divide(
    tape: TapeStack,
    quotient: Variable,
    remainder: Variable,
    dividend: Variable,
    divisor: Variable,
) -> str:
    has_remainder = tape.register_variable()

    def condition():
        return fn_greater_equals(tape, has_remainder, remainder, divisor)

    code = (
        fn_copy(tape, remainder, dividend)
        + op_clear(tape, quotient)
        + condition()
        + op_while(
            tape,
            has_remainder,
            lambda: (
                fn_minus(tape, remainder, remainder, divisor)
                + op_increment(tape, quotient)
                + condition()
            ),
        )
    )
    tape.unregister_variable(has_remainder)
    return code
