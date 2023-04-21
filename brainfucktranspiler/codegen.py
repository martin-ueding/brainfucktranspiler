import abc
from typing import Callable


class Variable:
    def __init__(self, name: str, position: int) -> None:
        self.name = name
        self.position = position


class TapeStack:
    def __init__(self) -> None:
        self._stack = []
        self._position = 0

    def register_variable(self, name: str) -> Variable:
        new_position = len(self._stack)
        new_variable = Variable(name, new_position)
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


def op_accumulate(tape: TapeStack, accumulator: Variable, summand: Variable) -> str:
    return op_while(
        tape,
        summand,
        lambda: (op_decrement(tape, summand) + op_increment(tape, accumulator)),
    )


def op_add(tape: TapeStack, result: Variable, left: Variable, right: Variable) -> str:
    return op_accumulate(tape, result, left) + op_accumulate(tape, result, right)


def op_clear(tape: TapeStack, var: Variable) -> str:
    return op_while(tape, var, lambda: op_decrement(tape, var))


def op_copy(tape: TapeStack, destination: Variable, source: Variable) -> str:
    temp = tape.register_variable("temp")
    code = (
        op_clear(tape, temp)
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


def op_multiply(
    tape: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    temp = tape.register_variable("temp")
    code = op_clear(tape, temp) + op_while(
        tape,
        left,
        lambda: (
            op_decrement(tape, left)
            + op_copy(tape, temp, right)
            + op_accumulate(tape, result, temp)
        ),
    )
    tape.unregister_variable(temp)
    return code
