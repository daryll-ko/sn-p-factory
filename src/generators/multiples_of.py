from src.classes.Neuron import Neuron
from src.classes.Position import Position
from src.classes.Rule import Rule
from src.classes.Synapse import Synapse
from src.classes.System import System


def generate_multiples_of_system(n: int) -> System:
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
