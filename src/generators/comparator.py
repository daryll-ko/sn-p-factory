from src.classes.Position import Position
from src.classes.Neuron import Neuron
from src.classes.Rule import Rule
from src.classes.System import System
from src.classes.Synapse import Synapse


def generate_comparator_system(a: int, b: int) -> System:
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
        Neuron(id="min", type_="output", position=Position(0, 0), rules=[], content=[]),
        Neuron(id="max", type_="output", position=Position(0, 0), rules=[], content=[]),
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
