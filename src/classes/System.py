from dataclasses import dataclass
from .Neuron import Neuron
from .Synapse import Synapse


@dataclass
class System:
    name: str
    neurons: list[Neuron]
    synapses: list[Synapse]
    input_neurons: list[int]
    output_neurons: list[int]
    spike_train: str
