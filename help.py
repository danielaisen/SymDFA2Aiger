from typing import List, Union


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


class TreeNode:
    def __init__(self, flag: bool = True, children: Union[List[int], List['TreeNode']] = None):
        """
        Initializes a tree node with a boolean flag and a list of children.

        Args:
            flag (bool): The boolean attribute of the node.
            children (Union[List[int], List['TreeNode']], optional): The list of children, which can be either a list of integers or a list of TreeNode instances. Default is None.
        """
        self.flag = flag
        self.children = children if children is not None else []

    def __repr__(self):
        """
        Returns a string representation of the tree node.
        """
        return f"TreeNode(flag={self.flag}, children={self.children})"
