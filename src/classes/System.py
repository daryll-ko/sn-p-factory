import re
import random

from collections import defaultdict
from dataclasses import dataclass
from .Neuron import Neuron
from .Rule import Rule


@dataclass
class System:
    name: str
    neurons: list[Neuron]

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "neurons": [neuron.to_dict() for neuron in self.neurons],
        }

    def to_dict_xmp(self) -> dict[str, any]:
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
                    list(map(lambda rule: rule.form_rule_xmp(), neuron.rules))
                ),
                "startingSpikes": neuron.spikes,
                "delay": neuron.downtime,
                "spikes": neuron.spikes,
            }

            if neuron.is_input:
                v["isInput"] = True
                v["bitstring"] = Neuron.decompress_spike_times(neuron.spike_times)

            if neuron.is_output:
                v["isOutput"] = True
                v["bitstring"] = Neuron.decompress_spike_times(neuron.spike_times)

            for synapse in neuron.synapses:
                if "out" not in v:
                    v["out"] = []
                if "outWeights" not in v:
                    v["outWeights"] = {}
                v["out"].append(id_to_label[synapse.to])
                v["outWeights"][id_to_label[synapse.to]] = synapse.weight

            neuron_entries.append((k, v))

        return {"content": dict(neuron_entries)}

    def simulate_one_step(self, time: int) -> bool:
        print()
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
        net_gain = [0 for _ in range(N)]

        for neuron in self.neurons:
            if neuron.is_input:
                if time in neuron.spike_times:
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
                for synapse in neuron.synapses:
                    to, w = synapse.to, synapse.weight
                    net_gain[to_index[to]] += rule.produced * w
                if neuron.is_output:
                    neuron.spike_times.append(time)
                neuron.downtime = rule.delay

        for neuron in self.neurons:
            if neuron.downtime == 0:
                neuron.spikes += net_gain[to_index[neuron.id]]
            neuron.downtime = max(neuron.downtime - 1, 0)

        return any(value != 0 for value in net_gain)
