
from help import TreeNode
from help import Index
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
from functools import singledispatch
from cnf import cnf
dictionary = {}
list_indexes = []


def _get(formula, neg):
    if str(formula) in dictionary:
        index = int(dictionary.get(str(formula)))
        return str(index) if not neg else str(index + 1)
    else:
        raise KeyError(
            f"Key '{str(formula)}' does not exist in the dictionary")


def helper_unaryop(formula: _UnaryOp, neg: bool = False):
    return _list(formula.argument, neg)


@singledispatch
def helper_list(formula: object):
    """finds the indexes of all proposition in the dictionary and return a list of them"""
    raise NotImplementedError(
        f"handler not implemented for object of type {type(formula)}"
    )


@helper_list.register
def helper_list(formula: object, dict):
    global dictionary
    dictionary = dict
    return _list(formula, None)


@singledispatch
def _list(formula: object, neg):
    """finds the indexes of all proposition in the dictionary and return a list of them"""
    raise NotImplementedError(
        f"handler not implemented for object of type {type(formula)}"
    )
# TODO make a outer function to assure I always get a tree back


@_list.register
def helper_atomic(formula: PropositionalTrue, neg):
    # this function is always being called within a AND operation.
    # AND true, is always the same value as without the TRUE.
    return None


@_list.register
def helper_atomic(formula: PLTLAtomic, neg):
    # node = TreeNode(neg, _get(formula, neg))
    # check if children == 1
    return _get(formula, neg)


@_list.register
def helper_not(formula: PLTLNot, neg):
    return helper_unaryop(formula, True)


@_list.register
def helper_and(formula: PLTLAnd, neg):
    l = [_list(f, None) for f in formula.operands]
    if neg is None:
        neg = False
    res = [i for i in l if i is not None]
    node = TreeNode(neg, res)
    return node


'''

a = PLTLAtomic("a")
b = PLTLAtomic("b")
c = PLTLAtomic("c")
d = PLTLAtomic("d")
neg = parse_pltl("!a")
_and = parse_pltl("a & b")
_and0 = parse_pltl("a & c")
_and1 = parse_pltl("a & b & !c")
_and2 = parse_pltl("!(a & b)")
_or = parse_pltl("a | b")
_or3 = parse_pltl("a | b | c ")
complex_1 = (Or(_and, _and0))
dic = {}
dic[str(a)] = 2
dic[str(b)] = 4
dic[str(c)] = 6
dictionary = dic

cnf1 = cnf(a)
tree = _list(cnf1, None)
# print(tree)

cnf1 = cnf(complex_1)
tree = _list(cnf1, None)
# print(tree)


cnf1 = cnf(_or)
# _list(cnf1, dic)


# Example usage:
# Creating a tree with integer children
node1 = TreeNode(True, [1, 2, 3])
# print(node1)  # Output: TreeNode(flag=True, children=[1, 2, 3])

# Creating a tree with nested TreeNode children
node2 = TreeNode(False, [TreeNode(True, [4, 5]), TreeNode(False, [6, 7])])
# Output: TreeNode(flag=False, children=[TreeNode(flag=True, children=[4, 5]), TreeNode(flag=False, children=[6, 7])])
# print(node2)

'''
