import re
import random

from heapq import heappush, heappop
from dataclasses import dataclass
from src.writes import write_json
from .Neuron import Neuron
from .Rule import Rule
from .Record import Record


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

        # for neuron in self.neurons:
        #     k = neuron.label
        #     v = {
        #         "id": neuron.label,
        #         "position": {
        #             "x": neuron.position[0],
        #             "y": neuron.position[1],
        #         },
        #         "rules": " ".join(
        #             list(map(lambda rule: rule.form_rule_xmp(), neuron.rules))
        #         ),
        #         "startingSpikes": neuron.spikes,
        #         "delay": neuron.downtime,
        #         "spikes": neuron.spikes,
        #     }

        #     if neuron.is_input:
        #         v["isInput"] = True
        #         v["bitstring"] = Neuron.decompress_log(neuron.spike_times)

        #     if neuron.is_output:
        #         v["isOutput"] = True
        #         v["bitstring"] = Neuron.decompress_log(neuron.spike_times)

        #     for synapse in neuron.synapses:
        #         if "out" not in v:
        #             v["out"] = []
        #         if "outWeights" not in v:
        #             v["outWeights"] = {}
        #         v["out"].append(id_to_label[synapse.to])
        #         v["outWeights"][id_to_label[synapse.to]] = synapse.weight

        #     neuron_entries.append((k, v))

        return {"content": dict(neuron_entries)}

    def log(self, time: int):
        dict_new = self.to_dict()
        write_json(dict_new, f"{self.name}@{str(time).zfill(3)}", True)

    def simulate(self) -> bool:
        to_index = {}
        for i, neuron in enumerate(self.neurons):
            to_index[neuron.id] = i

        incoming_spikes = [[] for _ in range(len(self.neurons))]  # @start of timestep

        time = 0
        done = False

        for neuron in self.neurons:
            if neuron.is_input:
                for record in neuron.input_log:
                    heappush(
                        incoming_spikes[to_index[neuron.id]],
                        (record.time, record.spikes),
                    )

        while not done and time < 10**3:
            for neuron in self.neurons:
                heap = incoming_spikes[to_index[neuron.id]]
                if neuron.downtime == 0:
                    while len(heap) > 0 and heap[0][0] == time:
                        neuron.spikes += heap[0][1]
                        heappop(heap)
                neuron.downtime = max(neuron.downtime - 1, 0)

            self.log(time)

            for neuron in self.neurons:
                if neuron.downtime == 0:
                    possible_indices = []

                    for index, rule in enumerate(neuron.rules):
                        python_regex = Rule.json_to_python_regex(rule.regex)
                        result = re.match(python_regex, "a" * neuron.spikes)
                        if result:
                            possible_indices.append(index)

                    if len(possible_indices) > 0:
                        chosen_index = random.choice(possible_indices)
                        rule = neuron.rules[chosen_index]
                        neuron.spikes -= rule.consumed
                        if rule.produced > 0:
                            for synapse in neuron.synapses:
                                to, weight = synapse.to, synapse.weight
                                heappush(
                                    incoming_spikes[to_index[to]],
                                    (time + rule.delay + 1, rule.produced * weight),
                                )
                            if neuron.is_output:
                                neuron.output_log.append(
                                    Record(time + rule.delay, rule.produced * weight)
                                )
                        neuron.downtime = rule.delay

            done = all([len(heap) == 0 for heap in incoming_spikes])
            time += 1

    def simulate_using_matrices(self):
        to_index = {}
        for j, neuron in enumerate(self.neurons):
            to_index[neuron.id] = j

        N = sum([len(neuron.rules) for neuron in self.neurons])
        M = len(self.neurons)

        P = [[0 for _ in range(M)] for _ in range(N)]  # production matrix (N×M)
        C = [[0 for _ in range(M)] for _ in range(N)]  # consumption matrix (N×M)

        offset = 0
        for j, neuron in enumerate(self.neurons):
            adjacent_indices = [to_index[synapse.to] for synapse in neuron.synapses]
            for i, rule in enumerate(neuron.rules):
                for adjacent_index in adjacent_indices:
                    P[offset + i][adjacent_index] = rule.produced
                C[offset + i][j] = rule.consumed
            offset += len(neuron.rules)

        time = 0

        while time < 10**3:
            # S = [0 for _ in range(M)]  # status vector (1×M)
            # I = [0 for _ in range(N)]  # indicator vector (1×N)

            # SP  # spiking vector (1×N)
            # G = I • P  # gain vector (1×N • N×M = 1×M)
            # L = SP • C  # loss vector (1×N • N×M = 1×M)

            # NG = S × (G - L) (1×M)
            # C_{k+1} - C_{k} = S × (G - L)
            # C_{k+1} = C_{k} + S × [(I • P) - (Sp • C)]

            # what's the difference between I and SP?

            time += 1
