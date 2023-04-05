from src.classes.System import System
from src.classes.Neuron import Neuron
from src.classes.Synapse import Synapse
from src.classes.Rule import Rule

import re


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


def parse_neuron(d: dict[str, any], to_id: dict[str, int]) -> Neuron:
    id = to_id[d["id"]]
    label = d["id"]
    position = round(float(d["position"]["x"])), round(float(d["position"]["y"]))
    rules = list(map(parse_rule, d["rules"].split())) if "rules" in d else []
    spikes = int(d["spikes"])
    downtime = int(d["delay"]) if "delay" in d else 0
    return Neuron(id, label, position, rules, spikes, downtime)


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

    neurons = []
    synapses = []
    input_neurons = []
    output_neurons = []
    spike_train = ""

    for v in d.values():
        neurons.append(parse_neuron(v, to_id))

    for v in d.values():
        id = to_id[v["id"]]

        if v["isInput"] == "true":
            input_neurons.append(id)

        if v["isOutput"] == "true":
            output_neurons.append(id)

        if "bitstring" in v and v["bitstring"]:
            spike_train = v["bitstring"]

        if "outWeights" in v:
            for inner_k, inner_v in v["outWeights"].items():
                start = id
                end = to_id[inner_k]
                weight = int(inner_v)
                synapses.append(Synapse(start, end, weight))

    return System(
        filename, neurons, synapses, input_neurons, output_neurons, spike_train
    )
