from classes.System import System
from classes.Neuron import Neuron
from classes.Synapse import Synapse
from classes.Rule import Rule

import re


def parse_xmp_dict(d: dict[str, any], filename: str) -> System:
    to_id = {}
    current_id = 0

    for k in d.keys():
        if k in to_id:
            print("Duplicate neuron found!")
            exit()
        else:
            to_id[k] = current_id
            current_id += 1

    name = filename
    neurons = []
    synapses = []
    input_neurons = []
    output_neurons = []
    spike_train = ""

    def get_symbol_value(s: str) -> int:
        if s == "0":
            return 0
        elif s == "a":
            return 1
        else:
            return int(s.replace("a", ""))

    def parse_rule(s: str) -> Rule:
        result = re.match("(.*)/(\d*a)->(\d*a|0);(\d+)", s)
        regex, consumed, produced, delay = result.groups()

        consumed = int(get_symbol_value(consumed))
        produced = int(get_symbol_value(produced))
        delay = int(delay)

        return Rule(regex, consumed, produced, delay)

    def parse_neuron_info(d: dict[str, any]) -> Neuron:
        id = to_id[d["id"]]
        label = d["id"]
        position = int(d["position"]["x"]), int(d["position"]["y"])
        rules = list(map(parse_rule, d["rules"].split()))
        spikes = int(d["spikes"])
        downtime = int(d["delay"])

        if bool(d["isInput"]):
            input_neurons.append(id)

        if bool(d["isOutput"]):
            output_neurons.append(id)

        if "bitstring" in d:
            global spike_train
            spike_train = d["bitstring"]

        for k, v in d["outWeights"]:
            start = id
            end = to_id[k]
            weight = v
            synapses.append(Synapse(start, end, weight))

        return Neuron(id, label, position, rules, spikes, downtime)

    for v in d.values():
        neurons.append(parse_neuron_info(v))

    return System(name, neurons, synapses, input_neurons, output_neurons, spike_train)
