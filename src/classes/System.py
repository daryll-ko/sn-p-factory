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

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "neurons": [neuron.to_dict() for neuron in self.neurons],
            "synapses": [synapse.to_dict() for synapse in self.synapses],
            "inputNeurons": self.input_neurons,
            "outputNeurons": self.output_neurons,
            "spikeTrain": self.spike_train,
        }
