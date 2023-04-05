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

    def to_dict_old(self) -> dict[str, any]:
        id_to_label = {}
        label_to_id = {}

        for neuron in self.neurons:
            id_to_label[neuron.id] = neuron.label
            label_to_id[neuron.label] = neuron.id

        neuron_entries = []

        for neuron in self.neurons:
            k = neuron.label
            v = {
                "id": neuron.label,
                "position": {
                    "x": neuron.position[0],
                    "y": neuron.position[1],
                },
                "rules": " ".join(
                    list(map(lambda rule: rule.form_rule_old(), neuron.rules))
                ),
                "startingSpikes": neuron.spikes,
                "delay": neuron.downtime,
                "spikes": neuron.spikes,
                "isOutput": neuron.id in self.output_neurons,
                "isInput": neuron.id in self.input_neurons,
            }
            if neuron.id in self.output_neurons:
                v["bitstring"] = ""
            for synapse in self.synapses:
                if synapse.start == label_to_id[k]:
                    if "out" not in v:
                        v["out"] = []
                    v["out"].append(id_to_label[synapse.end])
                    if "outWeights" not in v:
                        v["outWeights"] = {}
                    v["outWeights"][id_to_label[synapse.end]] = synapse.weight
                    break
            neuron_entries.append((k, v))

        return {"content": dict(neuron_entries)}
