"""
Functions for working with dictionary trees.

These are primarily designed to be used with keymap trees, but should function
with other dictionary based trees.

These functions do not cause any side effects (although some do mutate state
within their own scope), unlike basically every other function in this project.
Give them inputs, they will always give you the same output.
"""


import operator
from inspect import getdoc


def flatten_tree(tree):
    """
    Flatten a dictionary tree into a list.

    Args:
        tree: A tree constructed from nested dictionaries.

    Returns:
        A list of all the leafs in the tree.
    """
    # The base case, a leaf
    if not isinstance(tree, dict):
        # Tree is not actually a tree here.
        return [tree]

    flat_tree = []
    for i in tree.values():
        flat_tree += flatten_tree(i)
    return flat_tree


def flatten_tree_pairs(tree, keylist=None):
    """
    Flatten a dictionary tree into a list of paths and leafs.

    The lists are pairs. The first element of the pair is a list with all the
    keys to find the leaf; if a keymap is passed to this, this will be the
    keychord. The second element of the list is the leaf; if a keymap is passed
    to this, this will be the editing command.

    An example output of this function might look like:
    [[["C-x", "C-f"], find-file], [["C-x", "p", "f"], project-find-file]]

    Args:
        tree: A tree constructed from nested dictionaries.
        keylist: A list of dictionary keys representing the path taken at each
            node to reach the current node. Used for the recursive behavior.

    Returns:
        A list of tuples representing the data stored in the tree and the path
        required to get there.
    """
    # Empty list is a dangerous default, so work around that
    if keylist is None:
        keylist = []

    # The base case, a leaf
    if not isinstance(tree, dict):
        # Tree is not actually a tree here.
        return [[keylist, tree]]

    flat_tree = []
    for key, val in tree.items():
        flat_tree += flatten_tree_pairs(val, keylist + [key])
    return flat_tree


def flatten_nested_list(nested_list):
    """
    Flatten a list tree with arbitrary nesting.

    Args:
        nested_list: A list of lists (or not) to be flattened.

    Returns:
        A list without any nested lists in it, representing the flattened
        version of the nested_list.
    """
    # Handle the empty list
    if nested_list == []:
        return []
    # Base case: not a list
    if not isinstance(nested_list, list):
        return [nested_list]
    # car/cdr recursion... am I doing exercises from a Lisp textbook?
    return (flatten_nested_list(nested_list[0]) +
            flatten_nested_list(nested_list[1:]))


def list_to_dict(flat_list):
    """
    Unflatten a list into a dictionary.

    For example, if this is passed [1, 2, 3, 4] it will return {1: {2: {3: 4}}}

    Args:
        flat_list: A list (tuple, or some similar iterable) where every element
            is a hashable datatype that can be used as dict keys.

    Returns:
        A nested dictionary.
    """
    # Base case: 1 element left
    if len(flat_list) == 1:
        return flat_list[0]
    return {flat_list[0]: list_to_dict(flat_list[1:])}


def add_path_to_tree(path, tree):
    """
    Return result of adding a path to a tree.

    Does NOT modify the existing tree, rather returns the result.

    Args:
        path: A list (or similar iterable) where all but the last element are
            hashable datatypes that can be used as dictionary keys. The last
            element is the leaf and can be any type.
        tree: A dictionary tree to add an item to.

    Returns:
        A dictionary tree representing the new path added to it.
    """
    first = path[0]
    rest = path[1:]

    # Base case, we have the last key:val pair
    if len(path) == 2:
        return tree | {first: rest[0]}

    branch = tree.get(first)
    if isinstance(branch, dict):
        return tree | {first: add_path_to_tree(rest, branch)}

    # If the branch does not exist yet, it's easy!
    return tree | list_to_dict(path)


def build_tree_from_pairs(flat_tree_pairs):
    """
    Build a tree from a list of lists of nodes and leafs.

    This is the inverse of flatten_tree_pairs defined above.
    `build_tree_from_pairs(flatten_tree_pairs(tree))`
    should return the original tree.

    Args:
        flat_tree_pairs: A list of lists of a list of nodes and a leaf
            representing a flat form of a tree. It looks like this:
            [[[node1, node2,... nodeN], leaf],...]

    Returns:
        A nested dictionary tree.
    """
    paths = map(flatten_nested_list, flat_tree_pairs)

    tree = {}
    for path in paths:
        tree = add_path_to_tree(path, tree)
    return tree


def replace_in_tree(tree, item, replacement, test=operator.eq):
    """
    Replace all instances of an item in a dictionary tree.

    Allows for a specifiable comparison operator via the test argument. Accepts
    comparison operators that take two values.

    Args:
        tree: A tree constructed from nested dictionaries.
        item: An item in the tree to replace. Can be any datatype stored in
            in your tree. If the leaf of the tree is equal by the operator of
            choice, it is replaced.
        replacement: The replacement. Can be any datatype.
        test: A function of two arguments representing a comparison operator.
            Defaults to operator.eq.

    Returns:
        A tree constructed of nested dictionaries with all instances of item
        replaced with replacement.
    """
    flat_tree = flatten_tree_pairs(tree)

    new_flat_tree = []
    for path, leaf in flat_tree:
        if test(leaf, item):
            leaf = replacement
        new_flat_tree.append([path, leaf])

    return build_tree_from_pairs(new_flat_tree)


def merge_trees(tree1, tree2):
    """
    Recursively merge two trees.

    Values in tree1 are treated with higher priority over values in tree1.

    Args:
        tree1: A tree constructed from nested dictionaries.
        tree2: A tree constructed from nested dictionaries.

    Returns:
        A tree constructed from nested dictionaries represented the merged
        trees.
    """
    new_tree_flat = flatten_tree_pairs(tree1) + flatten_tree_pairs(tree2)
    return build_tree_from_pairs(new_tree_flat)


# Not a tree function, but rather a comparison operator that I will use
# with.

# This is a really bad workaround
def docstring_equal_p(func1, func2):
    """
    Compare the docstrings of two functions.

    Args:
        func1: A function.
        func2: A function.

    Returns:
        A bool representing if the docstrings are equal or not.
    """
    doc_func1 = getdoc(func1)
    doc_func2 = getdoc(func2)
    return doc_func1 == doc_func2
