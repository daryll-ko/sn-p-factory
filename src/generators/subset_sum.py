from src.classes.Position import Position
from src.classes.Neuron import Neuron
from src.classes.Rule import Rule
from src.classes.System import System
from src.classes.Synapse import Synapse


def generate_subset_sum_system(L: list[int], s: int) -> System:
    n = len(L)

    c = [
        Neuron(
            id="c_{0}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=1,
        )
    ] + [
        Neuron(
            id=f"c_{{{i}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a$", consumed=1, produced=1, delay=0),
                Rule(regex="^a$", consumed=1, produced=1, delay=1),
            ],
            content=1,
        )
        for i in range(1, n + 1)
    ]

    d = [
        Neuron(
            id=f"d_{{{i}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
                Rule(regex="^a$", consumed=1, produced=0, delay=0),
            ],
            content=0,
        )
        for i in range(1, n + 1)
    ]

    in_ = [
        Neuron(
            id=f"in_{{{i}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a(aa)+$", consumed=2, produced=1, delay=0)],
            content=2 * L[i - 1],
        )
        for i in range(1, n + 1)
    ] + [
        Neuron(
            id=f"in_{{{n+1}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a(aa)+$", consumed=2, produced=1, delay=0)],
            content=2 * s,
        )
    ]

    e = [
        Neuron(
            id=f"e_{{{i},{j}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        )
        for i in range(1, n + 1)
        for j in range(1, 3)
    ]

    h = [
        Neuron(
            id=f"h_{{{i}}}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=1 if i == 1 else 0,
        )
        for i in range(1, 6)
    ]

    g = [
        Neuron(
            id="g_{1}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a{2}$", consumed=2, produced=0, delay=0),
                Rule(regex="^a$", consumed=1, produced=1, delay=0),
            ],
            content=0,
        ),
        Neuron(
            id="g_{2}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a$", consumed=1, produced=1, delay=0),
                Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
            ],
            content=0,
        ),
        Neuron(
            id="g_{3}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(regex="^a$", consumed=1, produced=1, delay=0),
                Rule(regex="^a{2}$", consumed=2, produced=1, delay=0),
            ],
            content=0,
        ),
    ]

    t = [
        Neuron(
            id="t_{1}",
            type_="regular",
            position=Position(0, 0),
            rules=[
                Rule(
                    regex=f"^a{{{2 * t_ + 1}}}$",
                    consumed=2 * t_ + 1,
                    produced=0,
                    delay=0,
                )
                for t_ in range(1, n + 1)
            ]
            + [Rule(regex="^a$", consumed=1, produced=1, delay=0)],
            content=0,
        ),
        Neuron(
            id="t_{2}",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a{2}$", consumed=2, produced=1, delay=0)],
            content=0,
        ),
    ]

    acc = [
        Neuron(
            id="acc",
            type_="regular",
            position=Position(0, 0),
            rules=[Rule(regex="^a(aa)+$", consumed=2, produced=1, delay=0)],
            content=0,
        )
    ]

    c_to_d = [
        Synapse(from_=f"c_{{{i}}}", to=f"d_{{{i}}}", weight=1) for i in range(1, n + 1)
    ] + [Synapse(from_="c_{0}", to=f"d_{{{i}}}", weight=1) for i in range(1, n + 1)]

    d_to_in = [
        Synapse(from_=f"d_{{{i}}}", to=f"in_{{{i}}}", weight=1) for i in range(1, n + 1)
    ]

    in_to_e = [
        Synapse(from_=f"in_{{{i}}}", to=f"e_{{{i},{j}}}", weight=1)
        for i in range(1, n + 1)
        for j in range(1, 3)
    ]

    e_to_t1 = [
        Synapse(from_=f"e_{{{i},{j}}}", to="t_{1}", weight=1)
        for i in range(1, n + 1)
        for j in range(1, 3)
    ]

    e_to_acc = [
        Synapse(from_=f"e_{{{i},{j}}}", to="acc", weight=1)
        for i in range(1, n + 1)
        for j in range(1, 3)
    ]

    h_to_h = [
        Synapse(from_="h_{1}", to="h_{2}", weight=1),
        Synapse(from_="h_{2}", to="h_{3}", weight=1),
        Synapse(from_="h_{3}", to="h_{4}", weight=1),
        Synapse(from_="h_{3}", to="h_{5}", weight=1),
        Synapse(from_="h_{4}", to="h_{5}", weight=1),
        Synapse(from_="h_{5}", to="h_{4}", weight=1),
    ]

    t_to_t = [Synapse(from_="t_{1}", to="t_{2}", weight=1)]

    g_to_g = [
        Synapse(from_="g_{1}", to="g_{2}", weight=1),
        Synapse(from_="g_{1}", to="g_{3}", weight=1),
        Synapse(from_="g_{2}", to="g_{3}", weight=1),
        Synapse(from_="g_{3}", to="g_{2}", weight=1),
    ]

    rest = [
        Synapse(from_="h_{4}", to="t_{1}", weight=1),
        Synapse(from_="t_{1}", to="h_{4}", weight=1),
        Synapse(from_="t_{1}", to="h_{5}", weight=1),
        Synapse(from_="t_{2}", to="acc", weight=1),
        Synapse(from_="t_{2}", to=f"in_{{{n+1}}}", weight=1),
        Synapse(from_="acc", to="g_{1}", weight=1),
        Synapse(from_=f"in_{{{n+1}}}", to="g_{1}", weight=1),
    ]

    neurons = c + d + in_ + e + h + g + t + acc
    synapses = (
        c_to_d
        + d_to_in
        + in_to_e
        + e_to_t1
        + e_to_acc
        + h_to_h
        + t_to_t
        + g_to_g
        + rest
    )

    return System(neurons, synapses)
