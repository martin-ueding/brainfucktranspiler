class RightInfiniteTape:
    def __init__(self) -> None:
        self._tape = [0]
        self._cursor = 0

    def right(self) -> None:
        self._cursor += 1
        if self._cursor == len(self._tape):
            self._tape.append(0)

    def left(self) -> None:
        assert self._cursor > 0
        if self._cursor == len(self._tape) - 1 and self.is_zero():
            self._tape.pop()
        self._cursor -= 1

    def increment(self) -> None:
        self._tape[self._cursor] += 1

    def decrement(self) -> None:
        assert not self.is_zero()
        self._tape[self._cursor] -= 1

    def is_zero(self) -> int:
        return self.get() == 0

    def get(self) -> int:
        return self._tape[self._cursor]

    def set(self, number: int) -> None:
        self._tape[self._cursor] = number


class StateMachine:
    def __init__(self, program: str, inputs: list[int]) -> None:
        self._program = program
        self._inputs = inputs

        self._tape = RightInfiniteTape()
        self._program_counter = 0
        self._outputs = []

    def step(self) -> None:
        instruction = self._program[self._program_counter]
        if instruction == "+":
            self._tape.increment()
        elif instruction == "-":
            self._tape.decrement()
        elif instruction == ">":
            self._tape.right()
        elif instruction == "<":
            self._tape.left()
        elif instruction == ",":
            self._tape.set(self._inputs.pop(0))
        elif instruction == ".":
            self._outputs.append(self._tape.get())
        elif instruction == "[":
            if self._tape.is_zero():
                self._goto_bracket(forward=True)
        elif instruction == "]":
            if not self._tape.is_zero():
                self._goto_bracket(forward=False)

        self._program_counter += 1

    def run(self) -> list[int]:
        while self._program_counter != len(self._program):
            self.step()
        return self._outputs

    def _goto_bracket(self, forward: bool) -> None:
        my_bracket = "[" if forward else "]"
        target_bracket = "]" if forward else "["
        increment = 1 if forward else -1
        bracket_counter = 0
        while True:
            instruction = self._program[self._program_counter]
            if instruction == my_bracket:
                bracket_counter += 1
            elif instruction == target_bracket:
                bracket_counter -= 1
                if bracket_counter == 0:
                    break
            self._program_counter += increment
