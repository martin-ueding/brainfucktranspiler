import abc


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


def op_clear(tape_stack: TapeStack, var: Variable) -> str:
    return tape_stack.seek(var) + "[-]"


def op_input(tape_stack: TapeStack, var: Variable) -> str:
    return tape_stack.seek(var) + ","


def op_output(tape_stack: TapeStack, var: Variable) -> str:
    return tape_stack.seek(var) + "."


def op_accumulate(
    tape_stack: TapeStack, accumulator: Variable, summand: Variable
) -> str:
    return (
        tape_stack.seek(summand)
        + "["
        + "-"
        + tape_stack.seek(accumulator)
        + "+"
        + tape_stack.seek(summand)
        + "]"
    )


def op_add(
    tape_stack: TapeStack, result: Variable, left: Variable, right: Variable
) -> str:
    return op_accumulate(tape_stack, result, left) + op_accumulate(
        tape_stack, result, right
    )


def op_copy(tape_stack: TapeStack, destination: Variable, source: Variable) -> str:
    temp = tape_stack.register_variable("temp")
    code = (
        op_clear(tape_stack, temp)
        + tape_stack.seek(source)
        + "[-"
        + tape_stack.seek(destination)
        + "+"
        + tape_stack.seek(temp)
        + "+"
        + tape_stack.seek(source)
        + "]"
        + op_accumulate(tape_stack, source, temp)
    )
    tape_stack.unregister_variable(temp)
    return code
