import functools
import operator
from random import Random
from typing import Protocol

from src.classes.Neuron import Neuron
from src.classes.Position import Position
from src.classes.Rule import Rule
from src.classes.Synapse import Synapse
from src.classes.System import System


class SystemGenerator(Protocol):
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class Increment:
    def generate(self, *args) -> System:
        (n,) = map(int, args)
        neurons = [
            Neuron(
                id="L_{i}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=2,
            ),
            Neuron(
                id="L_{i,1}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=1)],
                content=0,
            ),
            Neuron(
                id="L_{i,2}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=1),
                ],
                content=0,
            ),
            Neuron(
                id="L_{i,3}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=0,
            ),
            Neuron(
                id="L_{i,4}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=0,
            ),
            Neuron(
                id="L_{j}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="L_{k}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="r",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a(a{2})+$", consumed=3, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=1),
                ],
                content=2 * n,
            ),
        ]

        synapses = [
            Synapse(from_="L_{i}", to="L_{i,1}", weight=1),
            Synapse(from_="L_{i}", to="L_{i,2}", weight=1),
            Synapse(from_="L_{i}", to="L_{i,3}", weight=1),
            Synapse(from_="L_{i}", to="L_{i,4}", weight=1),
            Synapse(from_="L_{i,1}", to="L_{j}", weight=1),
            Synapse(from_="L_{i,2}", to="L_{j}", weight=1),
            Synapse(from_="L_{i,2}", to="L_{k}", weight=1),
            Synapse(from_="L_{i,3}", to="L_{k}", weight=1),
            Synapse(from_="L_{i,3}", to="r", weight=1),
            Synapse(from_="L_{i,4}", to="r", weight=1),
        ]

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        return [rand.randint(0, 100)]


class Decrement:
    def generate(self, *args) -> System:
        (n,) = map(int, args)
        neurons = [
            Neuron(
                id="L_{i}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=2,
            ),
            Neuron(
                id="L_{i,1}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=0,
            ),
            Neuron(
                id="L_{i,2}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=1)],
                content=0,
            ),
            Neuron(
                id="L_{j}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="L_{k}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="r",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a(a{2})+$", consumed=3, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=1),
                ],
                content=2 * n,
            ),
        ]

        synapses = [
            Synapse(from_="L_{i}", to="L_{i,1}", weight=1),
            Synapse(from_="L_{i}", to="r", weight=1),
            Synapse(from_="L_{i}", to="L_{i,2}", weight=1),
            Synapse(from_="L_{i,1}", to="L_{j}", weight=1),
            Synapse(from_="L_{i,2}", to="L_{k}", weight=1),
            Synapse(from_="r", to="L_{j}", weight=1),
            Synapse(from_="r", to="L_{k}", weight=1),
        ]

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        return [rand.randint(0, 100)]


class SubsetSum:
    def generate(self, *args) -> System:
        s, *L = map(int, args)
        n = len(L)

        c = [
            Neuron(
                id="c_{0}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=1,
            )
        ] + [
            Neuron(
                id=f"c_{{{i}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=1),
                ],
                content=1,
            )
            for i in range(1, n + 1)
        ]

        d = [
            Neuron(
                id=f"d_{{{i}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            )
            for i in range(1, n + 1)
        ]

        in_ = [
            Neuron(
                id=f"in_{{{i}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a(a{2})+$", consumed=2, produced=1, delay=0)],
                content=2 * L[i - 1],
            )
            for i in range(1, n + 1)
        ] + [
            Neuron(
                id=f"in_{{{n+1}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a(a{2})+$", consumed=2, produced=1, delay=0)],
                content=2 * s,
            )
        ]

        e = [
            Neuron(
                id=f"e_{{{i},{j}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=0,
            )
            for i in range(1, n + 1)
            for j in range(1, 3)
        ]

        h = [
            Neuron(
                id=f"h_{{{i}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=1 if i == 1 else 0,
            )
            for i in range(1, 6)
        ]

        g = [
            Neuron(
                id="g_{1}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=0, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="g_{2}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="g_{3}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                ],
                content=0,
            ),
        ]

        t = [
            Neuron(
                id="t_{1}",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(
                        regex=f"^a{{{2 * t_ + 1}}}$",
                        consumed=2 * t_ + 1,
                        produced=0,
                        delay=0,
                    )
                    for t_ in range(1, n + 1)
                ]
                + [Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=0,
            ),
            Neuron(
                id="t_{2}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a{2}$", consumed=2, produced=1, delay=0)],
                content=0,
            ),
        ]

        acc = [
            Neuron(
                id="acc",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a(a{2})+$", consumed=2, produced=1, delay=0)],
                content=0,
            )
        ]

        c_to_d = [
            Synapse(from_=f"c_{{{i}}}", to=f"d_{{{i}}}", weight=1)
            for i in range(1, n + 1)
        ] + [Synapse(from_="c_{0}", to=f"d_{{{i}}}", weight=1) for i in range(1, n + 1)]

        d_to_in = [
            Synapse(from_=f"d_{{{i}}}", to=f"in_{{{i}}}", weight=1)
            for i in range(1, n + 1)
        ]

        in_to_e = [
            Synapse(from_=f"in_{{{i}}}", to=f"e_{{{i},{j}}}", weight=1)
            for i in range(1, n + 1)
            for j in range(1, 3)
        ]

        e_to_t1 = [
            Synapse(from_=f"e_{{{i},{j}}}", to="t_{1}", weight=1)
            for i in range(1, n + 1)
            for j in range(1, 3)
        ]

        e_to_acc = [
            Synapse(from_=f"e_{{{i},{j}}}", to="acc", weight=1)
            for i in range(1, n + 1)
            for j in range(1, 3)
        ]

        h_to_h = [
            Synapse(from_="h_{1}", to="h_{2}", weight=1),
            Synapse(from_="h_{2}", to="h_{3}", weight=1),
            Synapse(from_="h_{3}", to="h_{4}", weight=1),
            Synapse(from_="h_{3}", to="h_{5}", weight=1),
            Synapse(from_="h_{4}", to="h_{5}", weight=1),
            Synapse(from_="h_{5}", to="h_{4}", weight=1),
        ]

        t_to_t = [Synapse(from_="t_{1}", to="t_{2}", weight=1)]

        g_to_g = [
            Synapse(from_="g_{1}", to="g_{2}", weight=1),
            Synapse(from_="g_{1}", to="g_{3}", weight=1),
            Synapse(from_="g_{2}", to="g_{3}", weight=1),
            Synapse(from_="g_{3}", to="g_{2}", weight=1),
        ]

        rest = [
            Synapse(from_="h_{4}", to="t_{1}", weight=1),
            Synapse(from_="t_{1}", to="h_{4}", weight=1),
            Synapse(from_="t_{1}", to="h_{5}", weight=1),
            Synapse(from_="t_{2}", to="acc", weight=1),
            Synapse(from_="t_{2}", to=f"in_{{{n+1}}}", weight=1),
            Synapse(from_="acc", to="g_{1}", weight=1),
            Synapse(from_=f"in_{{{n+1}}}", to="g_{1}", weight=1),
        ]

        neurons = c + d + in_ + e + h + g + t + acc
        synapses = (
            c_to_d
            + d_to_in
            + in_to_e
            + e_to_t1
            + e_to_acc
            + h_to_h
            + t_to_t
            + g_to_g
            + rest
        )

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        n = rand.randint(1, 10)
        L = [rand.randint(1, 20) for _ in range(n)]
        return [sum(L) if rand.randint(0, 1) == 0 else rand.randint(1, 20), *L]


def reversed_bits(x: int) -> list[int]:
    L = []
    while x > 0:
        L.append(x % 2)
        x //= 2
    return L


class BitAdder:
    def generate(self, *args) -> System:
        L = [*map(int, args)]
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
            Neuron(
                id="out", type_="output", position=Position(0, 0), rules=[], content=[]
            )
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

    @staticmethod
    def rand_args(rand: Random) -> list:
        n = rand.randint(1, 10)
        return [rand.randint(1, 100) for _ in range(n)]


class MultiplesOf:
    def generate(self, *args) -> System:
        (n,) = map(int, args)

        neurons = [
            Neuron(
                id="1",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=1, produced=1, delay=n - 1),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=2,
            ),
            Neuron(
                id="2",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a$", consumed=1, produced=1, delay=n - 1),
                    Rule(regex="^a$", consumed=1, produced=1, delay=n),
                ],
                content=1,
            ),
            Neuron(
                id="3",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{3}$", consumed=3, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=n),
                    Rule(regex="^a{2}$", consumed=2, produced=0, delay=0),
                ],
                content=3,
            ),
            Neuron(
                id="env_{out}",
                type_="output",
                position=Position(0, 0),
                rules=[],
                content=[],
            ),
        ]

        synapses = [
            Synapse(from_="1", to="2", weight=1),
            Synapse(from_="1", to="3", weight=1),
            Synapse(from_="2", to="1", weight=1),
            Synapse(from_="2", to="3", weight=1),
            Synapse(from_="3", to="env_{out}", weight=1),
        ]

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        return [rand.randint(1, 100)]


def to_bool_list(n: int, bits: int) -> list[bool]:
    b = []
    while n > 0:
        b.append(n % 2 == 1)
        n //= 2
    while len(b) < bits:
        b.append(False)
    return b


class BoolFunction:
    def generate(self, *args) -> System:
        fun_str, *L = args
        L = [*map(int, L)]

        def fun(L):
            match fun_str:
                case "and":
                    return functools.reduce(operator.and_, L)
                case "xor":
                    return functools.reduce(operator.xor, L)
                case "sum_not_two":
                    return lambda L: sum(L) != 2
                case _:
                    raise Exception(":(")

        n = len(L)

        env_in = [
            Neuron(
                id=f"env_{{in_{{{i}}}}}",
                type_="input",
                position=Position(0, 0),
                rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
                content=[L[i]] * 5,
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
                        produced=1 if fun(to_bool_list(i, n)) else 0,
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

    @staticmethod
    def rand_args(rand: Random) -> list:
        ops = ["and", "xor", "sum_not_two"]
        op = rand.choice(ops)

        n = rand.randint(2, 5)
        L = [rand.randint(0, 1) for _ in range(n)]

        return [op, *L]


class Comparator:
    def generate(self, *args) -> System:
        (a, b) = map(int, args)
        neurons = [
            Neuron(
                id="a",
                type_="input",
                position=Position(0, 0),
                rules=[],
                content=[1 for _ in range(a)],
            ),
            Neuron(
                id="b",
                type_="input",
                position=Position(0, 0),
                rules=[],
                content=[1 for _ in range(b)],
            ),
            Neuron(
                id="both",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                    Rule(regex="^a$", consumed=1, produced=0, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="one",
                type_="regular",
                position=Position(0, 0),
                rules=[
                    Rule(regex="^a{2}$", consumed=2, produced=0, delay=0),
                    Rule(regex="^a$", consumed=1, produced=1, delay=0),
                ],
                content=0,
            ),
            Neuron(
                id="min", type_="output", position=Position(0, 0), rules=[], content=[]
            ),
            Neuron(
                id="max", type_="output", position=Position(0, 0), rules=[], content=[]
            ),
        ]

        synapses = [
            Synapse(from_="a", to="one", weight=1),
            Synapse(from_="a", to="both", weight=1),
            Synapse(from_="b", to="one", weight=1),
            Synapse(from_="b", to="both", weight=1),
            Synapse(from_="one", to="max", weight=1),
            Synapse(from_="both", to="min", weight=1),
            Synapse(from_="both", to="max", weight=1),
        ]

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        return [rand.randint(1, 20), rand.randint(1, 20)]


class CompleteGraph:
    def generate(self, *args) -> System:
        (n,) = map(int, args)

        neurons = [
            Neuron(
                id=f"n_{{{i}}}",
                type_="regular",
                position=Position(0, 0),
                rules=[Rule(regex="^a*$", consumed=1, produced=1, delay=0)],
                content=1,
            )
            for i in range(n)
        ]

        synapses = [
            Synapse(from_=f"n_{{{i}}}", to=f"n_{{{j}}}", weight=1)
            for i in range(n)
            for j in range(n)
            if i != j
        ]

        return System(neurons, synapses)

    @staticmethod
    def rand_args(rand: Random) -> list:
        return [rand.randint(1, 64)]


def str_to_generator(s: str) -> SystemGenerator:
    match s:
        case "increment":
            return Increment()
        case "decrement":
            return Decrement()
        case "bit_adder":
            return BitAdder()
        case "subset_sum":
            return SubsetSum()
        case "multiples_of":
            return MultiplesOf()
        case "bool_function":
            return BoolFunction()
        case "comparator":
            return Comparator()
        case "complete_graph":
            return CompleteGraph()
        case _:
            raise Exception(":(")
