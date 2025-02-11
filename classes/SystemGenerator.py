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
        (n,) = args
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
        (n,) = args
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


class BitAdder:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class SubsetSum:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class MultiplesOf:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class BoolFunction:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class Comparator:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


class CompleteGraph:
    def generate(self, *args) -> System: ...

    @staticmethod
    def rand_args(rand: Random) -> list: ...


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
