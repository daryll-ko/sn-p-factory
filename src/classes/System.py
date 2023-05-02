import re
import random

from collections import defaultdict
from dataclasses import dataclass
from .Neuron import Neuron
from .Rule import Rule
from .Synapse import Synapse
from .Terminal import Terminal


@dataclass
class System:
    name: str
    neurons: list[Neuron]
    synapses: list[Synapse]
    input_neurons: list[Terminal]
    output_neurons: list[Terminal]

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "neurons": [neuron.to_dict() for neuron in self.neurons],
            "synapses": [synapse.to_dict() for synapse in self.synapses],
            "inputNeurons": [
                input_neuron.to_dict() for input_neuron in self.input_neurons
            ],
            "outputNeurons": [
                output_neuron.to_dict() for output_neuron in self.output_neurons
            ],
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
            }

            for input_neuron in self.input_neurons:
                if neuron.id == input_neuron.id:
                    v["isInput"] = True
                    v["bitstring"] = Terminal.decompress(input_neuron.spike_times)

            for output_neuron in self.output_neurons:
                if neuron.id == output_neuron.id:
                    v["isOutput"] = True
                    v["bitstring"] = Terminal.decompress(output_neuron.spike_times)

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

    def simulate_one_step(self, time: int) -> bool:
        print(f"Time: {time}")
        print()
        print(f"System: {self}")

        to_index = defaultdict(int)
        current_index = 0

        for neuron in self.neurons:
            if neuron.id not in to_index:
                to_index[neuron.id] = current_index
                current_index += 1

        N = current_index
        adj_list = [[] for _ in range(N)]

        for synapse in self.synapses:
            adj_list[synapse.start].append((synapse.end, synapse.weight))

        net_gain = [0 for _ in range(N)]

        inputs = set()
        outputs = set()

        for input_neuron in self.input_neurons:
            inputs.add(input_neuron.id)
        for output_neuron in self.output_neurons:
            outputs.add(output_neuron.id)

        for neuron in self.neurons:
            if neuron.id in inputs:
                for input_neuron in self.input_neurons:
                    if neuron.id == input_neuron.id:
                        if time in input_neuron.spike_times:
                            neuron.spikes += 1
            i = to_index[neuron.id]
            possible_indices = []
            for index, rule in enumerate(neuron.rules):
                python_regex = Rule.get_python_regex(rule.regex)
                result = re.match(python_regex, "a" * neuron.spikes)
                if result:
                    possible_indices.append(index)
            if len(possible_indices) > 0:
                chosen_index = random.choice(possible_indices)
                rule = neuron.rules[chosen_index]
                net_gain[i] -= rule.consumed
                for j, w in adj_list[i]:
                    net_gain[j] += rule.produced * w
                if neuron.id in outputs:
                    for output_neuron in self.output_neurons:
                        if neuron.id == output_neuron.id:
                            output_neuron.spike_times.append(time)
                neuron.downtime += rule.delay

        for neuron in self.neurons:
            if neuron.downtime == 0:
                neuron.spikes += net_gain[to_index[neuron.id]]
            neuron.downtime = max(neuron.downtime - 1, 0)

        return any(value != 0 for value in net_gain)

    def simulate_completely(self):
        time = 0
        while self.simulate_one_step(time) and time < 2 * 10**4:
            time += 1
        return
