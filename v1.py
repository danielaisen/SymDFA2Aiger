
"""Modify the formula with base operators visitor."""
from pylogics_modalities.parsers import parse_pltl
from functools import singledispatch

from pylogics_modalities.syntax.base import And as PLTLAnd
from pylogics_modalities.syntax.base import Formula
from pylogics_modalities.syntax.base import Not as PLTLNot
from pylogics_modalities.syntax.base import Or as PLTLOr
from pylogics_modalities.syntax.base import _UnaryOp
from pylogics_modalities.syntax.pltl import Atomic as PLTLAtomic
from pylogics_modalities.syntax.pltl import (
    Before,
    WeakBefore,
    FalseFormula,
    PropositionalFalse,
    PropositionalTrue,
    Since,
    Triggers
)


class Index:
    def __init__(self, initial_value):
        self._i = initial_value
        self._i2 = initial_value * 2
        self._t2 = (initial_value - 1) * 2

    @property
    def i(self):
        return (self._i)

    @i.setter
    def i(self, value):
        self._i = value
        self._i2 = value * 2
        self._t2 = (value - 1) * 2

    @property
    def i2(self):
        return str(self._i2)

    @property
    def t2(self):
        return str(self._t2)


index = Index(1)

d = {}
a_ands = ""
lat = 0
ou = 0
an = 0


def aiger_action(sigma_controlled, sigma_environment):
    s_action = ""
    a_action = ""
    act = 0

    for action in sigma_controlled:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        s_action += 'i' + index.t2 + \
            " controllable_" + str(action) + '\n'
        index.i += 1
        act += 1
    for action in sigma_environment:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        s_action += 'i' + index.t2 + \
            ' i_' + str(action) + '\n'
        index.i += 1
        act += 1

    return s_action, a_action, act


def aiger_init():
    s_init = ""
    a_init = ""
    d["init"] = index.i2
    s_init += 'l' + index.t2 + "latch_init" + '\n'
    a_init += index.i2 + "1" + '\n'
    index.i += 1

    return s_init, a_init


def main():
    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    sigma_controlled = {a,  c}
    sigma_environment = {b}

    s_action, a_action, act = aiger_action(sigma_controlled, sigma_environment)
    s_init, a_init = aiger_init()

    print(index.i)
    print(index.i2)
    print(a_action)
    print(s_action)
    print(d)


if __name__ == "__main__":
    main()
