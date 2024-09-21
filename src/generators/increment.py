from src.classes.Neuron import Neuron
from src.classes.Position import Position
from src.classes.Rule import Rule
from src.classes.Synapse import Synapse
from src.classes.System import System


def generate_increment_system(initial_value: int) -> System:
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
            content=2 * initial_value,
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
