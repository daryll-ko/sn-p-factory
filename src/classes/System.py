from dataclasses import dataclass
from .Neuron import Neuron
from .Synapse import Synapse


@dataclass
class System:
    neurons: list[Neuron]
    synapses: list[Synapse]
    input_neuron: int
    output_neuron: int
