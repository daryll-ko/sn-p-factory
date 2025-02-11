import random
import re
from collections import Counter, defaultdict
from typing import Any, Literal

from .Neuron import Neuron
from .Synapse import Synapse


class System:
    neurons: list[Neuron]
    synapses: list[Synapse]

    _neuron_to_index: dict[str, int]
    _adjacency_list: list[list[Synapse]]
    _incoming_spikes: dict[int, dict[str, int]]
    _downtime: list[int]

    def __init__(self, neurons: list[Neuron], synapses: list[Synapse]) -> None:
        self.neurons = neurons
        self.synapses = synapses

        self._neuron_to_index = {}
        for i, neuron in enumerate(self.neurons):
            self._neuron_to_index[neuron.id] = i

        self._adjacency_list = [[] for _ in range(len(self.neurons))]
        for i, neuron in enumerate(self.neurons):
            self._adjacency_list[i] = self._get_synapses_from(neuron.id)

        self._incoming_spikes = defaultdict(lambda: defaultdict(int))

        self._downtime = [0 for _ in range(len(self.neurons))]

    def __repr__(self) -> str:
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        return {
            "neurons": [neuron.to_dict() for neuron in self.neurons],
            "synapses": [synapse.to_dict() for synapse in self.synapses],
        }

    def _get_synapses_from(self, from_: str) -> list[Synapse]:
        return list(filter(lambda synapse: synapse.from_ == from_, self.synapses))

    def _get_synapses_to(self, to: str) -> list[Synapse]:
        return list(filter(lambda synapse: synapse.to == to, self.synapses))

    @staticmethod
    def clean_xml_tag(s: str) -> str:
        cleaned = re.sub(",", "", re.sub("}", "", re.sub("{", "", s)))
        if re.match(r"^\d+", s):
            return f"n_{cleaned}"
        else:
            return f"{cleaned}"

    def to_dict_xml(self) -> dict[str, Any]:
        neuron_entries: list[tuple[str, dict[str, Any]]] = []

        for neuron in self.neurons:
            k = System.clean_xml_tag(neuron.id)
            v: dict[str, Any] = {
                "id": System.clean_xml_tag(neuron.id),
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
                v["delay"] = 0
            else:
                v["bitstring"] = (
                    ",".join(map(str, neuron.content))
                    if neuron.content is not None
                    else ""
                )

            if neuron.type_ == "input":
                assert isinstance(neuron.content, list)
                v["delay"] = 0
                v["isInput"] = True

            if neuron.type_ == "output":
                v["spikes"] = 0
                v["isOutput"] = True

            for synapse in self.synapses:
                if synapse.from_ == neuron.id:
                    if "out" not in v:
                        v["out"] = []
                    if "outWeights" not in v:
                        v["outWeights"] = {}
                    v["out"].append(System.clean_xml_tag(synapse.to))
                    v["outWeights"][System.clean_xml_tag(synapse.to)] = synapse.weight

            neuron_entries.append((k, v))

        return {"content": dict(neuron_entries)}

    def simulate(
        self,
        type_: Literal["generating", "halting", "boolean"],
        time_limit: int,
        make_log: bool,
    ):
        simulation_log: list[str] = []
        print_buffer: list[str] = []

        def flush_print_buffer() -> None:
            simulation_log.append("\n".join(print_buffer))
            print_buffer.clear()

        def capture_state() -> None:
            for i, neuron in enumerate(self.neurons):
                if neuron.type_ == "regular":
                    print_buffer.append(
                        f">> {neuron.id}\t<{neuron.content}/{self._downtime[i]}>"
                    )
                else:
                    print_buffer.append(f">> {neuron.id}\t{neuron.content}")

        start, end = -1, -1
        boolean_result = -1
        t = 0
        done = False

        for i, neuron in enumerate(self.neurons):
            if neuron.type_ == "input":
                assert isinstance(neuron.content, list)
                for t, spikes in enumerate(neuron.content):
                    if spikes > 0:
                        for synapse in self._adjacency_list[
                            self._neuron_to_index[neuron.id]
                        ]:
                            to, weight = synapse.to, synapse.weight
                            j = self._neuron_to_index[to]
                            self._incoming_spikes[t][to] += spikes

        while not done and t < time_limit:

            # = = = = = = = = = = = = = = = = = = = = = = = = =

            simulation_log.append(f"{t=}")
            simulation_log.append("> phase 1: incoming spikes")

            incoming_updates: Counter[str] = Counter()

            for neuron in self.neurons:
                i = self._neuron_to_index[neuron.id]
                if self._downtime[i] == 0:
                    if neuron.id in self._incoming_spikes[t]:
                        incoming_updates[neuron.id] += self._incoming_spikes[t][
                            neuron.id
                        ]
                        if neuron.type_ == "regular":
                            assert isinstance(neuron.content, int)
                            neuron.content += incoming_updates[neuron.id]

            for k, v in incoming_updates.items():
                print_buffer.append(f">> {k}\t{v}")

            if len(print_buffer) > 0:
                flush_print_buffer()
            else:
                simulation_log.append(">> no events during phase 1")

            # = = = = = = = = = = = = = = = = = = = = = = = = =

            simulation_log.append("> phase 2: showing starting state")

            capture_state()
            flush_print_buffer()

            # = = = = = = = = = = = = = = = = = = = = = = = = =

            simulation_log.append("> phase 3: selecting rules")

            some_rule_selected = False

            for i, neuron in enumerate(self.neurons):
                if neuron.type_ == "regular":
                    assert isinstance(neuron.content, int)

                    if self._downtime[i] == 0:
                        possible_rules = []

                        for j, rule in enumerate(neuron.rules):
                            result = re.match(rule.regex, "a" * neuron.content)
                            if result:
                                possible_rules.append(rule)

                        if len(possible_rules) > 0:
                            some_rule_selected = True
                            rule = random.choice(possible_rules)
                            print_buffer.append(f">> {neuron.id}: {rule}")

                            neuron.content -= rule.consumed
                            if rule.produced > 0:
                                for synapse in self._adjacency_list[
                                    self._neuron_to_index[neuron.id]
                                ]:
                                    to, weight = synapse.to, synapse.weight
                                    j = self._neuron_to_index[to]
                                    self._incoming_spikes[
                                        t
                                        + rule.delay
                                        + (
                                            1
                                            if self.neurons[j].type_ != "output"
                                            else 0
                                        )
                                    ][to] += (rule.produced * weight)

                            self._downtime[i] = rule.delay
                    else:
                        self._downtime[i] -= 1

            if len(print_buffer) > 0:
                flush_print_buffer()
            else:
                simulation_log.append(">> no events during phase 3")

            done = (
                all(len(d) == 0 for _t, d in self._incoming_spikes.items() if _t > t)
                and not some_rule_selected
            )

            # = = = = = = = = = = = = = = = = = = = = = = = = =

            simulation_log.append("> phase 4: accumulating updates, detecting outputs")

            output_detected = False

            for i, neuron in enumerate(self.neurons):
                if self._downtime[i] == 0:
                    if neuron.id in self._incoming_spikes[t]:
                        delta = self._incoming_spikes[t][neuron.id]
                        incoming_updates[neuron.id] += delta

                    if neuron.type_ == "output":
                        assert isinstance(neuron.content, list)
                        neuron.content.append(incoming_updates[neuron.id])
                        output_detected |= incoming_updates[neuron.id] > 0

            if len(print_buffer) > 0:
                flush_print_buffer()
            else:
                simulation_log.append(">> no events during phase 4")

            if type_ == "generating" and output_detected:
                if start == -1:
                    start = t
                    simulation_log.append(">> detected first output spike")
                else:
                    end = t
                    simulation_log.append(
                        ">> detected second output spike, wrapping up..."
                    )
                    break

            # = = = = = = = = = = = = = = = = = = = = = = = = =

            simulation_log.append("> phase 5: showing in-between state")

            capture_state()
            flush_print_buffer()

            if type_ == "boolean" and t == 3:
                boolean_result = output_detected
                break

            t += 1

        if make_log:
            for line in simulation_log:
                print(line)
                print()

        match type_:
            case "generating":
                if end == -1:
                    return -1
                else:
                    return end - start
            case "halting":
                return t
            case "boolean":
                return boolean_result

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
            adjacent_indices = [
                to_index[synapse.to] for synapse in self._get_synapses_from(neuron.id)
            ]
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

        raise NotImplementedError()
