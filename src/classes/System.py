import os
import re
import random
import shutil

from heapq import heappush, heappop
from dataclasses import dataclass
from typing import Any
from collections import Counter
from src.utils import write
from src.globals import XML
from .Neuron import Neuron
from .Synapse import Synapse
from .Format import Format
from .TestName import TestName


@dataclass
class System:
    neurons: list[Neuron]
    synapses: list[Synapse]

    def to_dict(self) -> dict[str, Any]:
        return {
            "neurons": [neuron.to_dict() for neuron in self.neurons],
            "synapses": [synapse.to_dict() for synapse in self.synapses],
        }

    def get_synapses_from(self, from_: str) -> list[Synapse]:
        return list(filter(lambda synapse: synapse.from_ == from_, self.synapses))

    def get_synapses_to(self, to: str) -> list[Synapse]:
        return list(filter(lambda synapse: synapse.to == to, self.synapses))

    @staticmethod
    def make_valid_xml_tag(s: str) -> str:
        return f"_{re.sub(',', '', re.sub('}', '', re.sub('{', '', s)))}"

    def to_dict_xml(self) -> dict[str, Any]:
        neuron_entries: list[tuple[str, dict[str, Any]]] = []

        for neuron in self.neurons:
            k = System.make_valid_xml_tag(neuron.id)
            v: dict[str, Any] = {
                "id": System.make_valid_xml_tag(neuron.id),
                "position": {
                    "x": neuron.position.x,
                    "y": neuron.position.y,
                },
            }

            if len(neuron.rules) > 0:
                v["rules"] = " ".join(
                    list(map(lambda rule: rule.stringify(in_xml=True), neuron.rules))
                )

            if isinstance(neuron.content, int):
                v["spikes"] = neuron.content
            else:
                v["bitstring"] = (
                    ",".join(map(str, neuron.content))
                    if neuron.content is not None
                    else ""
                )

            if neuron.type_ == "input":
                assert isinstance(neuron.content, list)
                v["isInput"] = True

            if neuron.type_ == "output":
                v["isOutput"] = True

            for synapse in self.synapses:
                if synapse.from_ == neuron.id:
                    if "out" not in v:
                        v["out"] = []
                    if "outWeights" not in v:
                        v["outWeights"] = {}
                    v["out"].append(System.make_valid_xml_tag(synapse.to))
                    v["outWeights"][
                        System.make_valid_xml_tag(synapse.to)
                    ] = synapse.weight

            neuron_entries.append((k, v))

        return {"content": dict(neuron_entries)}

    def simulate(self, filename: str, format: Format, verbose: bool):
        log_folder_name = filename.replace(" ", "_")
        log_folder_path = os.path.join(format.path, log_folder_name)

        if os.path.isdir(log_folder_path):
            shutil.rmtree(log_folder_path)

        to_index: dict[str, int] = {}
        for i, neuron in enumerate(self.neurons):
            to_index[neuron.id] = i

        incoming_spikes: list[list[tuple[int, int]]] = [
            [] for _ in range(len(self.neurons))
        ]

        downtime = [0 for _ in range(len(self.neurons))]

        time = 0
        done = False

        for i, neuron in enumerate(self.neurons):
            if neuron.type_ == "input":
                assert isinstance(neuron.content, list)
                for index, record in enumerate(neuron.content):
                    if record > 0:
                        for synapse in self.get_synapses_from(neuron.id):
                            to, weight = synapse.to, synapse.weight
                            j = to_index[to]
                            heappush(
                                incoming_spikes[j],
                                (index, record),
                            )

        simulation_log = []
        print_buffer = []

        start, end = -1, -1
        # output_at_3 = False

        while not done and time < 10**3:
            simulation_log.append(f"{'- ' * 15}time: {time} {'- '*15}\n")
            simulation_log.append("\n")
            simulation_log.append("> phase 1: incoming spikes\n")
            simulation_log.append("\n")

            incoming_updates: Counter[str] = Counter()

            for i, neuron in enumerate(self.neurons):
                heap = incoming_spikes[i]
                if downtime[i] == 0:
                    while len(heap) > 0 and heap[0][0] == time:
                        incoming_updates[neuron.id] += heap[0][1]
                        heappop(heap)
                    if neuron.type_ == "regular":
                        assert isinstance(neuron.content, int)
                        neuron.content += incoming_updates[neuron.id]

            for k, v in incoming_updates.items():
                print_buffer.append(f">> {k}: {v}")

            if len(print_buffer) > 0:
                for line in print_buffer:
                    simulation_log.append(f"{line}\n")
                print_buffer.clear()
            else:
                simulation_log.append(">> no events during phase 1\n")
            simulation_log.append("\n")

            simulation_log.append("> phase 2: logging state\n")
            simulation_log.append("\n")

            for neuron in self.neurons:
                if neuron.type_ == "regular":
                    print_buffer.append(
                        f">> {neuron.id}: <{neuron.content}/{downtime[i]}>"
                    )
                else:
                    print_buffer.append(f">> {neuron.id}: {neuron.content}")

            for line in print_buffer:
                simulation_log.append(f"{line}\n")
            print_buffer.clear()
            simulation_log.append("\n")

            log_testname = TestName(filename, time)
            log_filename = log_testname.make_filename()

            simulation_log.append(
                f">> logged to file ({log_filename}.{format.extension})\n"
            )
            simulation_log.append("\n")
            d = self.to_dict_xml() if format == XML else self.to_dict()
            write(d, log_filename, format, simulating=True)

            simulation_log.append("> phase 3: selecting rules\n")
            simulation_log.append("\n")

            for i, neuron in enumerate(self.neurons):
                if neuron.type_ == "regular":
                    assert isinstance(neuron.content, int)
                    if downtime[i] == 0:
                        possible_indices = []

                        for index, rule in enumerate(neuron.rules):
                            result = re.match(rule.regex, "a" * neuron.content)
                            if result:
                                possible_indices.append(index)

                        if len(possible_indices) > 0:
                            chosen_index = random.choice(possible_indices)
                            rule = neuron.rules[chosen_index]
                            print_buffer.append(f">> {neuron.id}: {rule}")

                            neuron.content -= rule.consumed
                            if rule.produced > 0:
                                for synapse in self.get_synapses_from(neuron.id):
                                    to, weight = synapse.to, synapse.weight
                                    j = to_index[to]
                                    heappush(
                                        incoming_spikes[j],
                                        (
                                            time
                                            + rule.delay
                                            + (
                                                1
                                                if self.neurons[j].type_ != "output"
                                                else 0
                                            ),
                                            rule.produced * weight,
                                        ),
                                    )
                                # if neuron.type_ == "output":
                                #     neuron.output_log.append(
                                #         Record(
                                #             time + rule.delay, rule.produced * weight
                                #         )
                                #     )

                            downtime[i] = rule.delay
                    else:
                        downtime[i] -= 1

            if len(print_buffer) > 0:
                for line in print_buffer:
                    simulation_log.append(f"{line}\n")
                print_buffer.clear()
            else:
                simulation_log.append(">> no events during phase 3\n")
            simulation_log.append("\n")

            simulation_log.append("> phase 4: detecting outputs\n")
            simulation_log.append("\n")

            output_detected = False

            for i, neuron in enumerate(self.neurons):
                heap = incoming_spikes[i]
                if downtime[i] == 0:
                    while len(heap) > 0 and heap[0][0] == time:
                        incoming_updates[neuron.id] += heap[0][1]
                        heappop(heap)
                    if neuron.type_ == "output":
                        assert isinstance(neuron.content, list)
                        neuron.content.append(incoming_updates[neuron.id])
                        output_detected |= incoming_updates[neuron.id] > 0

            # for i, neuron in enumerate(self.neurons):
            #     if (
            #         neuron.type_ == "output"
            #         and len(neuron.output_log) > 0
            #         and neuron.output_log[-1].time == time
            #     ):
            #         output_detected = True
            #         print_buffer.append(
            #             f">> {neuron.id}: {neuron.output_log[-1].spikes}"
            #         )

            if len(print_buffer) > 0:
                for line in print_buffer:
                    simulation_log.append(f"{line}\n")
                print_buffer.clear()
            else:
                simulation_log.append(">> no events during phase 4\n")
            simulation_log.append("\n")

            # if time == 3:
            #     output_at_3 = output_detected
            # elif time == 4:
            #     return output_at_3

            if output_detected:
                if start == -1:
                    start = time
                    simulation_log.append(">> detected first output spike\n")
                    simulation_log.append("\n")
                else:
                    end = time
                    simulation_log.append(
                        ">> detected second output spike, wrapping up...\n"
                    )
                    simulation_log.append("\n")
                    break

            simulation_log.append("> phase 5: showing in-between state\n")
            simulation_log.append("\n")

            for neuron in self.neurons:
                if neuron.type_ == "regular":
                    print_buffer.append(
                        f">> {neuron.id}: <{neuron.content}/{downtime[i]}>"
                    )
                else:
                    print_buffer.append(f">> {neuron.id}: {neuron.content}")

            for line in print_buffer:
                simulation_log.append(f"{line}\n")
            print_buffer.clear()
            simulation_log.append("\n")

            done = all([len(heap) == 0 for heap in incoming_spikes])
            time += 1

        if verbose:
            for line in simulation_log:
                print(line, end="")

        if end == -1:
            return -1
        else:
            return end - start

    # def simulate_using_matrices(self):
    #     to_index = {}
    #     for j, neuron in enumerate(self.neurons):
    #         to_index[neuron.id] = j

    #     N = sum([len(neuron.rules) for neuron in self.neurons])
    #     M = len(self.neurons)

    #     P = [[0 for _ in range(M)] for _ in range(N)]  # production matrix (N×M)
    #     C = [[0 for _ in range(M)] for _ in range(N)]  # consumption matrix (N×M)

    #     offset = 0
    #     for j, neuron in enumerate(self.neurons):
    #         adjacent_indices = [to_index[synapse.to] for synapse in neuron.synapses]
    #         for i, rule in enumerate(neuron.rules):
    #             for adjacent_index in adjacent_indices:
    #                 P[offset + i][adjacent_index] = rule.produced
    #             C[offset + i][j] = rule.consumed
    #         offset += len(neuron.rules)

    #     time = 0

    #     while time < 10**3:
    #         S = [0 for _ in range(M)]  # status vector (1×M)
    #         I = [0 for _ in range(N)]  # indicator vector (1×N)

    #         SP  # spiking vector (1×N)
    #         G = I • P  # gain vector (1×N • N×M = 1×M)
    #         L = SP • C  # loss vector (1×N • N×M = 1×M)

    #         NG = S × (G - L) (1×M)
    #         C_{k+1} - C_{k} = S × (G - L)
    #         C_{k+1} = C_{k} + S × [(I • P) - (Sp • C)]

    #         what's the difference between I and SP?

    #         time += 1
