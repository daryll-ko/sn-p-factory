from src.classes.Neuron import Neuron
from src.classes.Position import Position
from src.classes.Rule import Rule
from src.classes.Synapse import Synapse
from src.classes.System import System


def generate_complete_graph_system(n: int) -> System:
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
