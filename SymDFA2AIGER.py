
"""Modify the formula with base operators visitor."""
from multipledispatch import dispatch
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

from functools import singledispatch

from typing import List, Union
from pylogics_modalities.parsers import parse_pltl
from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Not as PLTLNot,
    _UnaryOp,
    Or
)
from pylogics_modalities.syntax.pltl import (
    Atomic as PLTLAtomic, PropositionalTrue

)


@singledispatch
def _list(formula: object):
    """finds the indexes of all proposition in the dictionary and return a list of them"""
    raise NotImplementedError(
        f"handler not implemented for object of type {type(formula)}"
    )


@_list.register
def helper_and(formula: PLTLAnd):
    l = [_list(f) for f in formula.operands]
    l_no_none = [i for i in l if i is not None]
    return _list(l_no_none)


@_list.register
def helper_atomic(formula: PropositionalTrue):
    return None


@_list.register
def helper_atomic(formula: PropositionalFalse):
    return 0


@_list.register
def helper_atomic(formula: PLTLAtomic):
    if str(formula) in dictionary:
        index = int(dictionary.get(str(formula)))
        return index
    else:
        raise KeyError(
            f"Key '{str(formula)}' does not exist in the dictionary")


@_list.register
def helper_not(formula: PLTLNot):
    return str(1 + int(_list(formula.argument)))


@_list.register
def aiger_ands(l: list):
    global a_ands, index, an, and_combination_dictionary

    def exist_in_and_dictionary(el1, el2):
        element1 = int(el1)
        element2 = int(el2)
        if element1 <= element2:
            key = f"{element1};{element2}"
            if key in and_combination_dictionary:
                return True, and_combination_dictionary[key]
            else:
                return False, None
        else:
            key = f"{element2};{element1}"
            if key in and_combination_dictionary:
                return True, and_combination_dictionary[key]
            else:
                return False, None

    def add_to_and_combination_dictionary(el1, el2, value):
        element1 = int(el1)
        element2 = int(el2)
        if element1 <= element2:
            key = f"{element1};{element2}"
            and_combination_dictionary[key] = value
        else:
            key = f"{element2};{element1}"
            and_combination_dictionary[key] = value

    def create_and(l):
        global a_ands, index, an
        if (len(l) == 1):
            last_element = l[0]
            return last_element
        temp_list = []
        length = len(l)
        i = 0
        while length >= 2:
            exist, value = exist_in_and_dictionary(l[i], l[i+1])
            if not exist:
                a_ands = a_ands + index.i2 + f" {l[i]} {l[i+1]}\n"
                add_to_and_combination_dictionary(l[i], l[i+1], index.i2)
                an += 1
                temp_list.append(index.i2)
                index.i += 1
                length -= 2
                i += 2
            else:
                temp_list.append(value)
                length -= 2
                i += 2
        if (length == 1):
            temp_list.append(l[i])
        return create_and(temp_list)
    return create_and(l)


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


def de_morgan_law(formula1, formula2):
    return (PLTLNot(PLTLAnd(PLTLNot(formula1), PLTLNot(formula2))))


def cnf_unaryop(formula: _UnaryOp):
    return cnf(formula.argument)


@singledispatch
def cnf(formula: object) -> Formula:
    """Rewrite a formula into conjunction normal form."""
    raise NotImplementedError(
        f"handler not implemented for object of type {type(formula)}"
    )


@cnf.register
def cnf_prop_true(formula: PropositionalTrue) -> Formula:
    return formula


@cnf.register
def cnf_prop_false(formula: PropositionalFalse) -> Formula:
    return formula


@cnf.register
def cnf_false(formula: FalseFormula) -> Formula:
    return formula


@cnf.register
def cnf_atomic(formula: PLTLAtomic) -> Formula:
    return formula


@cnf.register
def cnf_and(formula: PLTLAnd) -> Formula:
    sub = [cnf(f) for f in formula.operands]
    return PLTLAnd(*sub)


@cnf.register
def cnf_or(formula: PLTLOr) -> Formula:
    if len(formula.operands) == 2:
        sub0 = cnf(formula.operands[0])
        sub1 = cnf(formula.operands[1])
        return (de_morgan_law(sub0, sub1))
    sub = [(cnf(f)) for f in formula.operands[:-1]]
    head = cnf(PLTLOr(*sub))
    tail = cnf(formula.operands[-1])
    return de_morgan_law(head, tail)


@cnf.register
def cnf_not(formula: PLTLNot) -> Formula:
    sub = cnf_unaryop(formula)
    return PLTLNot(sub)


@cnf.register
def cnf_implies(formula: PLTLImplies) -> Formula:
    head = [PLTLNot(cnf(f)) for f in formula.operands[:-1]]
    tail = formula.operands[-1]
    return cnf(PLTLOr(*head, tail))


@cnf.register
def cnf_yesterday(formula: Before) -> Formula:
    return Before(cnf_unaryop(formula))


@cnf.register
def cnf_weak_yesterday(formula: WeakBefore) -> Formula:
    return WeakBefore(cnf_unaryop(formula))


@cnf.register
def cnf_since(formula: Since) -> Formula:
    sub = [cnf(f) for f in formula.operands]
    return Since(*sub)


@cnf.register
def cnf_since(formula: Triggers) -> Formula:
    sub = [cnf(f) for f in formula.operands]
    return Triggers(*sub)


@cnf.register
def cnf_once(formula: Once) -> Formula:
    return Once(cnf_unaryop(formula))


@cnf.register
def cnf_historically(formula: Historically) -> Formula:
    return Historically(cnf_unaryop(formula))


def aiger_action(sigma_controlled, sigma_environment):
    s_action = ""
    a_action = ""
    act = 0
    i_index = 0

    if (sigma_environment is not None) & (sigma_controlled is not None):
        if (len(sigma_controlled)+len(sigma_environment)) != len(sigma_environment.union(sigma_controlled)):
            raise NotImplementedError(
                f"The set of actions are not disjoint {sigma_controlled, sigma_environment}")

    if sigma_controlled is not None:
        for action in sigma_controlled:
            dictionary[str(action)] = index.i2
            a_action += index.i2 + '\n'
            s_action += f"i{i_index} controllable_{action}\n"
            index.i += 1
            act += 1
            i_index += 1
    if sigma_environment is not None:
        for action in sigma_environment:
            dictionary[str(action)] = index.i2
            a_action += index.i2 + '\n'
            s_action += f"i{i_index} i_{action}\n"
            index.i += 1
            act += 1
            i_index += 1
    return s_action, a_action, act


def aiger_init():
    global i0
    dictionary["Init"] = index.i2
    s_init = f"l{i0} latch_init\n"
    a_init = index.i2 + " 1" + '\n'
    index.i += 1
    global lat
    lat += 1

    return s_init, a_init


def aiger_out():
    s_out = ""
    a_out = ""
    dictionary["Output"] = index.i2
    s_out += "o0 F(X)"+'\n'
    a_out += index.i2 + '\n'
    index.i += 1

    return s_out, a_out


def aiger_final(final_state):
    f = dictionary.get('Output')
    init = dictionary.get('Init')
    phi = cnf(final_state)

    last_element = _list(phi)

    a_final = f"{f} {init} {last_element}\n"
    global an
    an += 1
    return a_final


def aiger_transition(initial_state, transition_system):
    initial_state_dict = {}
    global lat
    if isinstance(initial_state, PLTLAnd):
        for form in initial_state.operands:
            if isinstance(form, PLTLAtomic):
                initial_state_dict[form.name] = str(1)
            elif isinstance(form, PLTLNot):
                initial_state_dict[form.argument.name] = str(0)
    else:
        if isinstance(initial_state, PLTLAtomic):
            initial_state_dict[initial_state.name] = str(1)
        elif isinstance(initial_state, PLTLNot):
            initial_state_dict[initial_state.argument.name] = str(0)

    init = dictionary['Init']
    a_transition = ""

    for state_var in transition_system.keys():
        phi = cnf(transition_system.get(state_var))
        next_x = _list(phi)
        left = _list(
            [1+int(init), initial_state_dict[state_var[:-6]]])
        right = _list([init, next_x])
        value = 1 + \
            int(_list([1 + int(left), 1 + int(right)]))
        index = dictionary[state_var]
        a_transition = a_transition + str(index) + " " + str(value) + '\n'
        lat += 1
    return a_transition


def aiger_state_variables(state_var: set[str]):
    global i0, lat
    s_var = ""
    a_var = ""
    for v in state_var:
        var = str(v)
        dictionary[var] = index.i2
        s_var += f"l{i0} latch_{var}\n"
        i0 += 1
        index.i += 1
        a_var = a_var + index.t2 + " " + index.i2 + '\n'
        lat += 1

        x_prime = (var) + "_prime"
        dictionary[x_prime] = index.i2
        s_var += f"l{i0} latch_{x_prime}\n"
        i0 += 1
        index.i += 1
    return s_var, a_var


def create_aag_file(file_name, data):
    with open(f"experiments/{file_name}", "w") as file:
        file.write(data)


index = Index(1)

dictionary = {}
and_combination_dictionary = {}
a_ands = ""
c = "\n"
i0 = 0
lat = 0
an = 0


def initialize():
    global index, dictionary, and_combination_dictionary, a_ands, c, i0, lat, ou, an
    index = Index(1)
    dictionary = {}
    and_combination_dictionary = {}
    a_ands = ""
    c = "\n"
    i0 = 0
    lat = 0
    an = 0


def SymDFA2AIGER(sigma_controlled: set[Formula], sigma_environment: set[Formula], state_variables: set[Formula],
                 initial_state: PLTLAnd, transition_system: dict, final_state_variable: PLTLAnd, file_name: str = "SymbDFA_AIGER.aag", state_variables_return_dict: dict = None):
    initialize()
    global c
    s_action, a_action, act = aiger_action(sigma_controlled, sigma_environment)

    s_var, a_var = aiger_state_variables(state_variables)
    s_init, a_init = aiger_init()
    s_out, a_out = aiger_out()
    a_final = aiger_final(final_state_variable)
    a_transition = aiger_transition(initial_state, transition_system)

    M = act + lat + an
    ou = 1
    a_declaration = f"aag {M} {act} {lat} {ou} {an}\n"
    a_total = a_declaration + a_action + a_var + \
        a_init + a_transition + a_out + a_final + a_ands
    s_total = s_action + s_var + s_init+s_out + "c"

    if file_name == None:
        file_name = "SymbDFA_AIGER.aag"
    if not isinstance(file_name, str):
        file_name = "SymbDFA_AIGER.aag"
    if not file_name.endswith(".aag"):
        file_name = file_name + ".aag"

    add_comments(state_variables, initial_state, transition_system,
                 final_state_variable,  state_variables_return_dict)
    create_aag_file(file_name, a_total + s_total + c)


def add_comments(state_variables, initial_state, transition_system, final_state_variable, state_variables_return_dict):
    global c
    if not state_variables_return_dict == None:
        if isinstance(state_variables_return_dict, dict):
            c = c + f"\n---state var:\n"
            for var in state_variables:
                c = c + f"{var}: {state_variables_return_dict[var]}\n"

    c = c + \
        f"\n---\ninitial state:\n{initial_state} \n---\ntransition relation:\n"
    for tran in transition_system.keys():
        c = c + f"{tran} iff {transition_system[tran]}\n"
    c = c + f"---\nfinal state: \n{final_state_variable}\n"
