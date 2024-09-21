from typing import Callable

from src.classes.Neuron import Neuron
from src.classes.Position import Position
from src.classes.Rule import Rule
from src.classes.Synapse import Synapse
from src.classes.System import System


def to_bool_list(n: int, bits: int) -> list[bool]:
    b = []
    while n > 0:
        b.append(n % 2 == 1)
        n //= 2
    while len(b) < bits:
        b.append(False)
    return b


def generate_boolean_function_system(
    b: list[bool], f: Callable[[list[bool]], bool]
) -> System:
    n = len(b)

    env_in = [
        Neuron(
            id=f"env_{{in_{{{i}}}}}",
            type_="input",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=[1 if b[i] else 0] * 5,
        )
        for i in range(n)
    ]

    in_ = [
        Neuron(
            id=f"in_{{{i}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        )
        for i in range(n)
    ]

    intermediate = [
        Neuron(
            id=f"{i},{j}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        )
        for i in range(n)
        for j in range(1 << i)
    ]

    auxiliary = [
        Neuron(
            id="aux_{0}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=1,
        ),
        Neuron(
            id="aux_{1}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=1,
        ),
        Neuron(
            id="aux_{2}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        ),
        Neuron(
            id="aux_{3}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        ),
    ]

    out = [
        Neuron(
            id="out",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(
                    regex=f"^a{{{i+1}}}$" if i > 0 else "^a$",
                    consumed=i + 1,
                    produced=1 if f(to_bool_list(i, n)) else 0,
                    delay=0,
                )
                for i in range(1 << n)
            ],
            content=0,
        )
    ]

    env_out = [
        Neuron(
            id="env_{out}",
            type_="output",
            position=Position(0, 0),
            rules=[],
            content=[],
        )
    ]

    env_in_to_in = [
        Synapse(from_=f"env_{{in_{{{i}}}}}", to=f"in_{{{i}}}", weight=1)
        for i in range(n)
    ]

    in_to_intermediate = [
        Synapse(from_=f"in_{{{i}}}", to=f"{i},{j}", weight=1)
        for i in range(n)
        for j in range(1 << i)
    ]

    intermediate_to_out = [
        Synapse(from_=f"{i},{j}", to="out", weight=1)
        for i in range(n)
        for j in range(1 << i)
    ]

    rest = [
        Synapse(from_="aux_{0}", to="aux_{1}", weight=1),
        Synapse(from_="aux_{1}", to="aux_{0}", weight=1),
        Synapse(from_="aux_{1}", to="aux_{2}", weight=1),
        Synapse(from_="aux_{2}", to="aux_{3}", weight=1),
        Synapse(from_="aux_{3}", to="out", weight=1),
        Synapse(from_="out", to="env_{out}", weight=1),
    ]

    neurons = env_in + in_ + intermediate + auxiliary + out + env_out
    synapses = env_in_to_in + in_to_intermediate + intermediate_to_out + rest

    return System(neurons, synapses)
