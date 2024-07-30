
"""Modify the formula with base operators visitor."""
from help import TreeNode
from pylogics_modalities.parsers import parse_pltl

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
transition_system = {}
a_ands = ""
lat = 0
ou = 0
an = 0
m = 0


# def aiger_ands(l: TreeNode, i: int, a_an: str = "", an: int = 0):
def aiger_ands(l: TreeNode):
    global a_ands, index, an
    last_element = index.t2

    def create_and(l):
        global a_ands, index, an
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
        global a_ands, index, an
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
        return last_element
    return traves_children(l)


def aiger_action(sigma_controlled, sigma_environment):
    s_action = ""
    a_action = ""
    act = 0
    i0 = 0

    for action in sigma_controlled:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        # s_action += 'i' + i0 + " controllable_" + str(action) + '\n'
        s_action += f"i{i0} controllable_{action}\n"
        index.i += 1
        act += 1
        i0 += 1
    for action in sigma_environment:
        d[str(action)] = index.i2
        a_action += index.i2 + '\n'
        # s_action += 'i' + index.t2 + ' i_' + str(action) + '\n'
        s_action += f"i{i0} i_{action}\n"
        index.i += 1
        act += 1
        i0 += 1
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
    init = d.get('Init')
    phi = cnf(final_state)
    # TODO check if there is better way then passing the dictionary
    l = helper_list(phi, d)

    last_element = str(aiger_ands(l))

    a_final = str(f) + ' ' + init + ' ' + last_element + '\n'
    global an
    an += 1
    return a_final


def aiger_transition(initial_state, transition_system):
    initial_state_dict = {}
    for form in initial_state.operands:
        if isinstance(form, PLTLAtomic):
            initial_state_dict[initial_state.operands[1]
                               .name] = d[initial_state.operands[1].name]
        elif isinstance(form, PLTLNot):
            initial_state_dict[initial_state.operands[2].argument.name] = str(
                1 + int(d[initial_state.operands[2].argument.name]))
        # there might also be a true element, but given it is in a AND operation we neglect it.

    init = d['Init']
    a_transition = ""

    for state_var in transition_system.keys():
        phi = cnf(transition_system.get(state_var))
        print(phi)
        l = helper_list(phi, d)
        next_x = str(aiger_ands(l))
        # state_var[:-6] for deleting the '_prime' string
        left = aiger_ands(
            TreeNode(False, [1+int(init), initial_state_dict[state_var[:-6]]]))
        right = aiger_ands(TreeNode(False, [init, next_x]))
        value = 1 + \
            int(aiger_ands(TreeNode(False, [1 + int(left), 1 + int(right)])))
        index = d[state_var]
        a_transition = a_transition + str(index) + " " + str(value) + '\n'
    return a_transition


@dispatch(list, Index)
def aiger_state_variables(state_var: list[str], index_temp: Index = None,):
    global index
    s_var = ""
    a_var = ""
    i0 = 0
    for v in state_var:
        var = str(v)
        d[var] = index.i2
        # s_var += 'l' + index.t2 + " latch_" + (var) + '\n'
        s_var += f"l{i0} latch_{var}\n"
        i0 += 1
        index.i += 1
        a_var = a_var + index.t2 + " " + index.i2 + '\n'

        x_prime = (var) + "_prime"
        d[x_prime] = index.i2
        # s_var += 'l' + index.i2 + " latch_" + x_prime + '\n'
        s_var += f"l{i0} latch_{x_prime}\n"
        i0 += 1
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
    i0 = 0
    for key in keys:

        var = str(key)
        d[var] = index.i2
        # s_var += 'l' + index.t2 + " latch_" + (var) + '\n'
        s_var += f"l{i0} latch_{var}\n"
        i0 += 1
        index.i += 1
        a_var = a_var + index.t2 + " " + index.i2 + '\n'

        x_prime = (var) + "_prime"
        d[x_prime] = index.i2
        # s_var += 'l' + index.i2 + " latch_" + x_prime + '\n'
        s_var += f"l{i0} latch_{x_prime}\n"

        i0 += 1

        index.i += 1

        comments += var + " maps to " + str(state_var[key]) + '\n'

    return s_var, a_var, comments


def main():
    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    _x1 = parse_pltl("x_var1")
    _x2 = parse_pltl("x_var2")

    # temp
    d["x_var1"] = '100'
    d["x_var2"] = '102'
    # temp
    sigma_controlled = {a, c}
    sigma_environment = {b}
    final_state_variable = PLTLAnd(_x1, _x2)
    state_variables = [_x1, _x2]
    initial_state = PLTLAnd(parse_pltl("true"), _x1, PLTLNot(_x2))

    transition_system["x_var1_prime"] = parse_pltl("(false | a | b | c)")
    transition_system["x_var2_prime"] = parse_pltl(" (true & (! a) & ! c )")

    s_action, a_action, act = aiger_action(sigma_controlled, sigma_environment)

    # s_action, a_action, comments = aiger_state_variables(state_variables, "Yesterday", "WeakYesterday")
    s_var, a_var, comments = aiger_state_variables(state_variables)
    s_init, a_init = aiger_init()
    s_out, a_out = aiger_out()
    a_final = aiger_final(final_state_variable)
    a_transition = aiger_transition(initial_state, transition_system)

    M = act + lat + ou + an
    a_declaration = f"aag {M} {act} {lat} {an} \n"
    a_total = a_declaration + a_action + a_var + \
        a_init + a_transition + a_out + a_final + a_ands
    s_total = s_action + s_var + s_init+s_out + "c \n"

    # Specify the filename with the .aag extension
    filename = "SymbDFA_AIGER.aag"

    # Open the file in write mode and write the content to it
    with open(filename, "w") as file:
        file.write(a_total + s_total)

    print(index.i)
    print(index.i2)
    print()
    print(a_action + a_init + a_out)
    print(s_action)
    print(d)


if __name__ == "__main__":
    main()

'''
index.i = 4
node1 = TreeNode(True, [2, 4, 6])

aaa = aiger_ands(node1)
print(aaa)
'''
