from .codegen import TapeStack, op_add, op_copy


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
