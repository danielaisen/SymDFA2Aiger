# SymDFA2Aiger
The logic library is currently compiled locally and can be found under the folder dist. 
Use pip install to install pylogics_modalities with all the relevant classes. 

pip install dist/pylogics_modalities-0.2.2-py3-none-any.whl


pip install multipledispatch
from multipledispatch import dispatch




"""Modify the formula with base operators visitor."""
# from help import TreeNode
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

from SymDFA2AIGER import SymDFA2AIGER


def main():

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
                 initial_state, transition_system, final_state_variable)

    print("done")


if __name__ == "__main__":
    main()
