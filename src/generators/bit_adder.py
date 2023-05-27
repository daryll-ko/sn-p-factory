from src.classes.Position import Position
from src.classes.Neuron import Neuron
from src.classes.Rule import Rule
from src.classes.System import System
from src.classes.Synapse import Synapse


def reversed_bits(x: int) -> list[int]:
    L = []
    while x > 0:
        L.append(x % 2)
        x //= 2
    return L


def generate_bit_adder_system(L: list[int]) -> System:
    n = len(L)

    in_ = [
        Neuron(
            id=f"in_{{{i}}}",
            type_="input",
            position=Position(0, 0),
            rules=[],
            content=reversed_bits(L[i]),
        )
        for i in range(n)
    ]

    stalls = [
        Neuron(
            id=f"stall_{{{i},{j}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        )
        for i in range(2, n)
        for j in range(i - 1)
    ]

    adders = [
        Neuron(
            id=f"add_{{{','.join([str(j) for j in range(i+2)])}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a$", consumed=1, produced=1, delay=0),
                Rule(regex="^a{2}$", consumed=1, produced=0, delay=0),
                Rule(regex="^a{3}$", consumed=2, produced=1, delay=0),
            ],
            content=0,
        )
        for i in range(n - 1)
    ]

    out = [
        Neuron(id="out", type_="output", position=Position(0, 0), rules=[], content=[])
    ]

    from_in = [
        Synapse(from_="in_{0}", to="add_{0,1}", weight=1),
        Synapse(from_="in_{1}", to="add_{0,1}", weight=1),
    ] + [
        Synapse(
            from_=f"in_{{{i}}}",
            to=f"stall_{{{i},0}}",
            weight=1,
        )
        for i in range(2, n)
    ]

    from_stall = [
        Synapse(from_=f"stall_{{{i},{j}}}", to=f"stall_{{{i},{j+1}}}", weight=1)
        for i in range(2, n)
        for j in range(i - 2)
    ] + [
        Synapse(
            from_=f"stall_{{{i},{i-2}}}",
            to=f"add_{{{','.join([str(j) for j in range(i+1)])}}}",
            weight=1,
        )
        for i in range(2, n)
    ]

    cascade = [
        Synapse(
            from_=f"add_{{{','.join([str(j) for j in range(i+1)])}}}",
            to=f"add_{{{','.join([str(j) for j in range(i+2)])}}}",
            weight=1,
        )
        for i in range(1, n - 1)
    ] + [
        Synapse(
            from_=f"add_{{{','.join([str(i) for i in range(n)])}}}",
            to="out",
            weight=1,
        )
    ]

    neurons = in_ + stalls + adders + out
    synapses = from_in + from_stall + cascade

    return System(neurons, synapses)
