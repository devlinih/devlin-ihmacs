"""
Functions for working with dictionary trees.

These are primarily designed to be used with keymap trees, but should function
with other dictionary based trees.

All of these functions are PURE! They do not cause any side effects, unlike
basically every other function in this project.
"""


def flatten_tree(tree):
    """
    Flatten a dictionary tree into a list.

    Args:
        tree: A tree constructed from nested dictionaries.

    Returns:
        A list of all the leafs in the tree.
    """
    pass


def flatten_tree_tuples(tree):
    """
    Flatten a dictionary tree into a list of tuples.

    The tuples are pairs. The first element of the pair is a list with all the
    keys to find the leaf. The second element of the tuple is the leaf.

    Args:
        tree: A tree constructed from nested dictionaries.
        keylist: A list of dictionary keys representing the path taken to reach
            the current node.

    Returns:
        A list of tuples representing the data stored in the tree and the path
        required to get there.
    """
    pass


def replace_in_tree(tree, item, replacement):
    """
    Replace all instances of an item in a dictionary tree.

    Args:
        tree: A tree constructed from nested dictionaries.
        item: An item in the tree to replace. Can be any datatype stored in
            in your tree. If the leaf of the tree is equal
            (by the == operator), it will be replaced.
        replacement: The replacement. Can be any datatype.

    Returns:
        A tree constructed of nested dictionaries with all instances of item
        replaced with replacement.
    """
    pass


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
    pass
