import re
import random

from heapq import heappush, heappop
from dataclasses import dataclass
from collections import defaultdict
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

    def log_json(self, filename: str):
        dict_new = self.to_dict()
        write_json(dict_new, filename, True)

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

        print_buffer = []

        while not done and time < 10:
            print("- " * 15, end="")
            print(f"time: {time}", end=" ")
            print("- " * 15)
            print()
            print("> phase 1: incoming spikes")
            print()

            incoming_updates = defaultdict(int)

            for neuron in self.neurons:
                heap = incoming_spikes[to_index[neuron.id]]
                if neuron.downtime == 0:
                    while len(heap) > 0 and heap[0][0] == time:
                        incoming_updates[neuron.id] += heap[0][1]
                        neuron.spikes += heap[0][1]
                        heappop(heap)

            for k, v in incoming_updates.items():
                print_buffer.append(f">> {k}: +{v}")

            if len(print_buffer) > 0:
                print("\n".join(print_buffer))
                print()
                print_buffer.clear()
            else:
                print(">> no events during phase 1")
                print()

            print("> phase 2: logging state")
            print()

            for neuron in self.neurons:
                print_buffer.append(
                    f">> {neuron.id}: <{neuron.spikes}/{neuron.downtime}>"
                )

            print("\n".join(print_buffer))
            print()
            print_buffer.clear()

            log_filename = f"{self.name.replace(' ', '_')}@{str(time).zfill(3)}"
            print(f">> logged to json file ({log_filename}.json)")
            print()
            self.log_json(log_filename)

            print("> phase 3: selecting rules")
            print()

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
                        print_buffer.append(f">> {neuron.id}: {rule}")
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
                else:
                    neuron.downtime -= 1

            if len(print_buffer) > 0:
                print("\n".join(print_buffer))
                print()
                print_buffer.clear()
            else:
                print(">> no events during phase 3")
                print()

            print("> phase 4: showing in-between state")
            print()

            for neuron in self.neurons:
                print_buffer.append(
                    f">> {neuron.id}: <{neuron.spikes}/{neuron.downtime}>"
                )

            print("\n".join(print_buffer))
            print()
            print_buffer.clear()

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
