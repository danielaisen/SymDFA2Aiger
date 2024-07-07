
"""Modify the formula with base operators visitor."""
from help import TreeNode
from pylogics_modalities.parsers import parse_pltl
from functools import singledispatch

from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Or as PLTLOr,
    Formula,
    Implies as PLTLImplies,
    Not as PLTLNot,
    _UnaryOp,
    Equivalence as PLTLEquivalence

)
from pylogics_modalities.syntax.pltl import (
    Atomic as PLTLAtomic,
    Before,
    WeakBefore,
    FalseFormula,
    Historically,
    Once,
    PropositionalFalse,
    PropositionalTrue,
    Since,
    Triggers,
    # PLTLEquivalence
)

from cnf import cnf
from helper_list import helper_list

from help import Index
from multipledispatch import dispatch


index = Index(1)

d = {}
a_ands = ""
lat = 0
ou = 0
an = 0


# def aiger_ands(l: TreeNode, i: int, a_an: str = "", an: int = 0):
def aiger_ands(l: TreeNode):
    global a_ands, index, an
    last_element = index.t2

    def create_and(l):
        global a_ands, index, an, last_element
        if (len(l) == 1):
            last_element = l[0]
            return last_element
        temp_list = []
        length = len(l)
        i = 0
        while length >= 2:
            a_ands = a_ands + index.i2 + ' ' + \
                str(l[i]) + ' ' + str(l[i+1]) + '\n'
            an += 1
            temp_list.append(index.i2)
            index.i += 1
            length -= 2
            i += 2
        if (length == 1):
            temp_list.append(l[i])
        return create_and(temp_list)

    def traves_children(t: TreeNode):
        global a_ands, index, an, last_element
        neg = l.flag
        if len(l.children) == 1:
            return l.children[0] + 1 if neg else l.children[0]
        int_list = []
        for child in l.children:
            if isinstance(child, int):
                int_list.append(child)
            elif isinstance(child, str):
                int_list.append(child)
            elif isinstance(child, TreeNode):
                traves_children(child)
        element = create_and(int_list)
        last_element = str(int(element)+1) if neg else element
    traves_children(l)
    return last_element


index.i = 4
node1 = TreeNode(True, [2, 4, 6])

aaa = aiger_ands(node1)
print(aaa)


def aiger_action(sigma_controlled, sigma_environment):
    s_action = ""
    a_action = ""
    act = 0

    for action in sigma_controlled:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        s_action += 'i' + index.t2 + " controllable_" + str(action) + '\n'
        index.i += 1
        act += 1
    for action in sigma_environment:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        s_action += 'i' + index.t2 + ' i_' + str(action) + '\n'
        index.i += 1
        act += 1

    return s_action, a_action, act


def aiger_init():
    d["Init"] = index.i2
    s_init = 'l' + index.t2 + " latch_init" + '\n'
    a_init = index.i2 + " 1" + '\n'
    index.i += 1
    global lat
    lat += 1

    return s_init, a_init


def aiger_out():
    s_out = ""
    a_out = ""
    d["Output"] = index.i2
    s_out += "o0 F(X)"+'\n'
    a_out += index.i2 + '\n'
    index.i += 1

    return s_out, a_out


def aiger_final(final_state):
    f = d.get('Output')
    phi = cnf(final_state)
    # TODO check if there is better way then passing the dictionary
    l = helper_list(phi, d)

    last_element = str(aiger_ands(l))
    a_final = str(f) + ' ' + last_element + ' ' + last_element + '/n'
    return a_final


@dispatch(list, Index)
def aiger_state_variables(state_var: list[str], index_temp: Index = None,):
    global index
    s_var = ""
    a_var = ""
    for v in state_var:
        var = str(v)
        d[var] = index.i2
        s_var += 'l' + index.t2 + " latch_" + (var) + '\n'
        index.i += 1
        a_var = a_var + index.t2 + " " + index.i2 + '\n'

        x_prime = (var) + "_prime"
        d[x_prime] = index.i2
        s_var += 'l' + index.i2 + " latch_" + x_prime + '\n'
        index.i += 1
    comments = 'c'
    return s_var, a_var, comments


@dispatch(list)
def aiger_state_variables(state_var: list[str]):
    i = Index(0)
    return aiger_state_variables(state_var, i)


@dispatch(dict, str, str, Index)
def aiger_state_variables(state_var: dict, keys1: str = None, keys2: str = None,  index_temp: Index = None,):
    global index
    s_var = ""
    a_var = ""
    keys = []
    if keys1 is not None:
        keys += state_var[keys1]
    if keys2 is not None:
        keys += state_var[keys2]
    if len(keys) == 0:
        keys = state_var.keys

    comments = ""
    for key in keys:

        var = str(key)
        d[var] = index.i2
        s_var += 'l' + index.t2 + " latch_" + (var) + '\n'
        index.i += 1
        a_var = a_var + index.t2 + " " + index.i2 + '\n'

        x_prime = (var) + "_prime"
        d[x_prime] = index.i2
        s_var += 'l' + index.i2 + " latch_" + x_prime + '\n'
        index.i += 1

        comments += var + " maps to " + str(state_var[key]) + '\n'

    return s_var, a_var, comments


def main():
    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    _x1 = parse_pltl("_x1")
    _x2 = parse_pltl("_x2")

    # temp
    d["_x1"] = '100'
    d["_x2"] = '102'
    # temp
    sigma_controlled = {a, c}
    sigma_environment = {b}
    final_state_variable = PLTLAnd(_x1, _x2)
    state_variables = [_x1, _x2]

    s_action, a_action, act = aiger_action(sigma_controlled, sigma_environment)

    # s_action, a_action, comments = aiger_state_variables(state_variables, "Yesterday", "WeakYesterday")
    s_action, a_action, comments = aiger_state_variables(state_variables)
    s_init, a_init = aiger_init()
    s_out, a_out = aiger_out()
    a_final = aiger_final(final_state_variable)
    # 3 aiger-transition

    print(index.i)
    print(index.i2)
    print()
    print(a_action + a_init + a_out)
    print(s_action)
    print(d)


if __name__ == "__main__":
    main()
