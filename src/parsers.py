from src.classes.System import System
from src.classes.Neuron import Neuron
from src.classes.Synapse import Synapse
from src.classes.Position import Position
from src.classes.Rule import Rule

import re


def parse_rule_xmp(s: str) -> Rule:
    result = re.match("(.*)/(\d*a)->(\d*a|0);(\d+)", s)
    regex, consumed, produced, delay = result.groups()

    consumed = int(Rule.get_value(consumed))
    produced = int(Rule.get_value(produced))
    delay = int(delay)

    return Rule(regex, consumed, produced, delay)


def parse_neuron_xmp(
    d: dict[str, any], to_id: dict[str, int], spike_train: list[int], is_output: bool
) -> Neuron:
    id = to_id[d["id"]]
    label = d["id"]
    position = Position(
        round(float(d["position"]["x"])), round(float(d["position"]["y"]))
    )
    rules = list(map(parse_rule_xmp, d["rules"].split())) if "rules" in d else []
    spikes = int(d["spikes"])
    downtime = int(d["delay"]) if "delay" in d else 0
    is_input = len(spike_train) > 0

    synapses = []

    if "outWeights" in d:
        for inner_k, inner_v in d["outWeights"].items():
            to = to_id[inner_k]
            weight = int(inner_v)
            synapses.append(Synapse(to, weight))

    return Neuron(
        id,
        label,
        position,
        rules,
        spikes,
        downtime,
        synapses,
        is_input,
        is_output,
        spike_train,
    )


def parse_dict_xmp(d: dict[str, any], filename: str) -> System:
    to_id = {}
    current_id = 0

    for k in d.keys():
        if k in to_id:
            print("Duplicate neuron found!")
            exit()
        else:
            to_id[k] = current_id
            current_id += 1

    input_neurons = dict()
    environment_neurons = set()
    output_neurons = set()

    for v in d.values():
        if "isInput" in v and v["isInput"] and "outWeights" in v and "bitstring" in v:
            for inner_k in v["outWeights"].keys():
                input_neurons[to_id[inner_k]] = Neuron.compress_to_spike_train(
                    v["bitstring"]
                )
        if "isOutput" in v and v["isOutput"]:
            environment_neurons.add(to_id[v["id"]])

    for v in d.values():
        if "outWeights" in v:
            for inner_k in v["outWeights"].keys():
                if inner_k in environment_neurons:
                    output_neurons.add(to_id[v["id"]])

    filtered_dicts = list(
        filter(
            lambda dict: not (
                ("isInput" in dict and dict["isInput"])
                or ("isOutput" in dict and dict["isOutput"])
            ),
            d.values(),
        )
    )

    neurons = [
        parse_neuron_xmp(
            v,
            to_id,
            input_neurons[to_id[v["id"]]] if to_id(v["id"]) in input_neurons else [],
            to_id[v["id"]] in output_neurons,
        )
        for v in filtered_dicts
    ]

    return System(filename, neurons)


def parse_position(d: dict[str, any]) -> Position:
    x = int(d["x"])
    y = int(d["y"])

    return Position(x, y)


def parse_rule(d: dict[str, any]) -> Rule:
    regex = d["regex"]
    consumed = int(d["consumed"])
    produced = int(d["produced"])
    delay = int(d["delay"])

    return Rule(regex, consumed, produced, delay)


def parse_neuron(d: dict[str, any]) -> Neuron:
    id = int(d["id"])
    label = d["label"]
    position = parse_position(d["position"])
    rules = [parse_rule(rule) for rule in d["rules"]]
    spikes = int(d["spikes"])
    downtime = int(d["downtime"])

    return Neuron(id, label, position, rules, spikes, downtime)


def parse_synapse(d: dict[str, any]) -> Neuron:
    start = int(d["from"])
    end = int(d["to"])
    weight = int(d["weight"])

    return Synapse(start, end, weight)


def parse_dict(d: dict[str, any]) -> System:
    name = d["name"]
    neurons = [parse_neuron(neuron) for neuron in d["neurons"]]

    return System(name, neurons)
