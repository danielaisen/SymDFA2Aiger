"""Modify the formulas to be of an instance of conjunction normal form (cnf) where no disjunction exist"""

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
        sub0 = formula.operands[0]
        sub1 = formula.operands[1]
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


# @cnf.register
# def cnf_equivalence(formula: PLTLEquivalence) -> Formula:
#    positive = PLTLAnd(*[cnf(f) for f in formula.operands])
#    negative = PLTLAnd(*[PLTLNot(cnf(f)) for f in formula.operands])
#    return PLTLEquivalence(sub = [cnf(f) for f in formula.operands])


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


'''
a = PLTLAtomic("xa")
b = PLTLAtomic("b")
c = PLTLAtomic("c")
d = PLTLAtomic("d")
neg = parse_pltl("!a")
_and = parse_pltl("a & b")
_or = parse_pltl("_X | b")
_or3 = parse_pltl("a | b | c ")
'''
# print(cnf(_or))
# print(cnf(_or3))
