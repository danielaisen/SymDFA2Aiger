from pylogics_modalities.parsers import parse_pltl

from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Not as PLTLNot)

from SymDFA2AIGER import SymDFA2AIGER


def call_AIGER():

    a = parse_pltl("a")
    _x1 = parse_pltl("x_var1")
    transition_system_input = {}
    sigma_controlled = {a}
    sigma_environment = None
    final_state_variable = _x1

    state_variables_input = [_x1]
    initial_state_input = _x1
    transition_system_input["x_var1_prime"] = parse_pltl("a")

    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input,
                 initial_state_input, transition_system_input, final_state_variable, "luca.aag")

    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    d = parse_pltl("d")
    _x1 = parse_pltl("x_var1")
    _x2 = parse_pltl("x_var2")
    _x3 = parse_pltl("x_var3")
    _x4 = parse_pltl("x_var4")

    sigma_controlled = {a, c}
    sigma_environment = {b, d}

    initial_state_input = PLTLAnd(_x1, PLTLNot(_x2), _x3, _x4)
    final_state_variable = PLTLAnd(_x1, _x2, PLTLNot(_x3), PLTLNot(_x4))
    state_variables_input = [_x1, _x2, _x3, _x4]

    transition_system_input = {}
    transition_system_input["x_var1_prime"] = parse_pltl("a")
    transition_system_input["x_var2_prime"] = parse_pltl("b")
    transition_system_input["x_var3_prime"] = parse_pltl("(false|a|(b&d)|!c)")
    transition_system_input["x_var4_prime"] = parse_pltl(" ((! a) & ! c )")

    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input,
                 initial_state_input, transition_system_input, final_state_variable, "experiment_aiger.aag")

    a = parse_pltl("a")
    _x1 = parse_pltl("x_var1")
    transition_system_input = {}
    sigma_controlled = {a}
    sigma_environment = None
    final_state_variable = (_x1)

    # state_variables_input = [_x1]
    state_variables_input = ["x_var1"]

    initial_state_input = (PLTLNot(_x1))
    transition_system_input["x_var1_prime"] = parse_pltl("a")

    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input,
                 initial_state_input, transition_system_input, final_state_variable, "file2")

    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    d = parse_pltl("d")
    _x1 = parse_pltl("x_var1")
    _x2 = parse_pltl("x_var2")
    _x3 = parse_pltl("x_var3")
    _x4 = parse_pltl("x_var4")
    transition_system_input = {}

    sigma_controlled = {a, c}
    # sigma_controlled = {a}
    sigma_environment = {b, d}
    # sigma_environment = {b}
    # sigma_environment = None

    # final_state_variable = PLTLAnd(_x1, _x2, PLTLNot(_x3), PLTLNot(_x4))
    final_state_variable = PLTLAnd(_x1, PLTLNot(_x2), _x3)

    state_variables_input = [_x1, _x2, _x3, _x4]
    initial_state_input = PLTLAnd(_x1, PLTLNot(_x2), _x3, _x4)
    # initial_state_input = PLTLNot((_x1))
    # initial_state_input = PLTLAnd(parse_pltl("true"), _x1, PLTLNot(
    #    _x2), PLTLAnd(parse_pltl("true"), _x1, PLTLNot(_x2)))

    transition_system_input["x_var1_prime"] = parse_pltl("a | b | c")
    transition_system_input["x_var2_prime"] = parse_pltl("b")

    transition_system_input["x_var3_prime"] = parse_pltl(
        "(false | a | (b & d) | !c)")
    transition_system_input["x_var4_prime"] = parse_pltl(
        " ((! a) & ! c )")

    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input,
                 initial_state_input, transition_system_input, final_state_variable)

    a = parse_pltl("a")
    b = parse_pltl("b")
    c = parse_pltl("c")
    _x1 = parse_pltl("x_var1")
    _x2 = parse_pltl("x_var2")
    transition_system = {}

    sigma_controlled = {a, c}
    sigma_environment = {b}
    final_state_variable = PLTLAnd(_x1, _x2)
    state_variables = [_x1, _x2]
    initial_state = PLTLAnd(parse_pltl("true"), _x1, PLTLNot(_x2))

    transition_system["x_var1_prime"] = parse_pltl("(false | a | b | c)")
    transition_system["x_var2_prime"] = parse_pltl(" (true & (! a) & ! c )")

    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables,
                 initial_state, transition_system, final_state_variable, "test simple")

    print("done")


if __name__ == "__main__":
    call_AIGER()
