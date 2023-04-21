from .interpreter import RightInfiniteTape, StateMachine


def test_tape_increment() -> None:
    tape = RightInfiniteTape()

    tape.increment()
    assert not tape.is_zero()
    tape.decrement()
    assert tape.is_zero()


def test_tape_movement() -> None:
    tape = RightInfiniteTape()

    tape.right()
    assert tape._tape == [0, 0]
    tape.increment()
    assert tape._tape == [0, 1]
    tape.left()
    assert tape._tape == [0, 1]
    tape.right()
    assert tape._tape == [0, 1]
    tape.decrement()
    assert tape._tape == [0, 0]
    tape.left()
    assert tape._tape == [0]


def test_state_machine() -> None:
    program = """
    >, >,           Accept two inputs into T1 and T2

    <               Goto T1
    [               While T1 is nonzero
        >               Goto T2
        [->+>+<<]       Copy T2 to T3 and T4
        >>              Goto to T4
        [-<<+>>]        Move T4 to T2
        <               Goto to T3
        [-<<<+>>>]      Accumulate T3 onto T0
        <<              Goto to T1
        -               Decrement T1
    ]

    <.              Emit T0
    """
    sm = StateMachine(program=program, inputs=[2, 3])
    result = sm.run()
    assert result == [6]
