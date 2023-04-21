from brainfucktranspiler.codegen import (
    TapeStack,
    op_input,
    op_output,
    op_while,
    fn_divide,
    op_if,
    fn_or,
    fn_plus,
    op_decrement,
    fn_not,
)
from brainfucktranspiler.interpreter import StateMachine


def test_euler_1() -> None:
    tape = TapeStack()
    result = tape.register_variable()
    divisor_1 = tape.register_variable()
    divisor_2 = tape.register_variable()
    ceiling = tape.register_variable()

    quotient = tape.register_variable()
    remainder = tape.register_variable()
    is_divisible_by_3 = tape.register_variable()
    is_divisible_by_5 = tape.register_variable()
    is_divisible_by_either = tape.register_variable()

    def loop_body() -> str:
        return (
            fn_divide(tape, quotient, remainder, ceiling, divisor_1)
            + fn_not(tape, is_divisible_by_3, remainder)
            + fn_divide(tape, quotient, remainder, ceiling, divisor_2)
            + fn_not(tape, is_divisible_by_5, remainder)
            + fn_or(tape, is_divisible_by_either, is_divisible_by_3, is_divisible_by_5)
            + op_if(
                tape,
                is_divisible_by_either,
                lambda: fn_plus(tape, result, result, ceiling),
            )
            + op_decrement(tape, ceiling)
        )

    code = (
        op_input(tape, divisor_1)
        + op_input(tape, divisor_2)
        + op_input(tape, ceiling)
        + op_decrement(tape, ceiling)
        + op_while(tape, ceiling, loop_body)
        + op_output(tape, result)
    )

    assert StateMachine(code, [3, 5, 10]).run() == [23]
