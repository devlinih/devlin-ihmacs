"""
Test tree helper functions.
"""


import pytest

import tree_helpers


# Large test trees
TEST_TREE_1 = (
    {"a": "self_insert_command",
     "C-j": "newline",
     "DEL": "backwards_delete_char",
     "KEY_DC": "delete_char",
     "C-d": "delete_char",
     "C-f": "forward_char",
     "KEY_RIGHT": "forward_char",
     "M-f": "forward_word",
     "C-b": "backward_char",
     "KEY_LEFT": "backward_char",
     "M-b": "backward_word",
     "C-n": "next_line",
     "KEY_DOWN": "next_line",
     "C-p": "previous_line",
     "KEY_UP": "previous_line",
     "C-a": "move_beginning_of_line",
     "KEY_HOME": "move_beginning_of_line",
     "C-e": "move_end_of_line",
     "KEY_END": "move_end_of_line",
     "C-v": "scroll_up",
     "KEY_NPAGE": "scroll_up",
     "M-v": "scroll_down",
     "KEY_PPAGE": "scroll_down",
     "C-x": {"C-f": "find_file",
             "C-c": "kill_ihmacs",
             "p": {"f": "project_find_file",
                   "p": "project_switch_project", }, },
     "C-c": {"C-c": "send_buffer",
             "m": "mu4e", }, }  # Kinda silly to put mu4e here honestly
)

TEST_FLAT_TREE_PAIRS_1 = (
    [[["a"], "self_insert_command"],
     [["C-j"], "newline"],
     [["DEL"], "backwards_delete_char"],
     [["KEY_DC"], "delete_char"],
     [["C-d"], "delete_char"],
     [["C-f"], "forward_char"],
     [["KEY_RIGHT"], "forward_char"],
     [["M-f"], "forward_word"],
     [["C-b"], "backward_char"],
     [["KEY_LEFT"], "backward_char"],
     [["M-b"], "backward_word"],
     [["C-n"], "next_line"],
     [["KEY_DOWN"], "next_line"],
     [["C-p"], "previous_line"],
     [["KEY_UP"], "previous_line"],
     [["C-a"], "move_beginning_of_line"],
     [["KEY_HOME"], "move_beginning_of_line"],
     [["C-e"], "move_end_of_line"],
     [["KEY_END"], "move_end_of_line"],
     [["C-v"], "scroll_up"],
     [["KEY_NPAGE"], "scroll_up"],
     [["M-v"], "scroll_down"],
     [["KEY_PPAGE"], "scroll_down"],
     [["C-x", "C-f"], "find_file"],
     [["C-x", "C-c"], "kill_ihmacs"],
     [["C-x", "p", "f"], "project_find_file"],
     [["C-x", "p", "p"], "project_switch_project"],
     [["C-c", "C-c"], "send_buffer"],
     [["C-c", "m"], "mu4e"]]
)


# Test cases
flatten_tree_cases = [
    # Test an empty dict
    ({}, []),
    # Test some single level "trees"
    ({"hello": "world",
      "one": 1,
      "two": 2, },
     ["world", 1, 2]),
    ({"tuple": (1, 2),
      "list": [1, 2],
      "dict": {1: 2},
      "int": 12, },
     [(1, 2), [1, 2], 2, 12]),
    # Test a tree with some light nesting
    ({"C-x": {"C-f": "find_file",
              "C-b": "switch_to_buffer",
              "C-c": "kill_ihmacs"},
      "C-f": "forward_char"},
     ["find_file", "switch_to_buffer", "kill_ihmacs", "forward_char"]),
    # Test an incomplete tree, leaves are empty dicts
    ({"C-x": {},
      "C-f": "forward_char"},
     ["forward_char"]),
    # Test a large test tree
    (TEST_TREE_1,
     ["self_insert_command", "newline", "backwards_delete_char", "delete_char",
      "delete_char", "forward_char", "forward_char", "forward_word",
      "backward_char", "backward_char", "backward_word", "next_line",
      "next_line", "previous_line", "previous_line", "move_beginning_of_line",
      "move_beginning_of_line", "move_end_of_line", "move_end_of_line",
      "scroll_up", "scroll_up", "scroll_down", "scroll_down", "find_file",
      "kill_ihmacs", "project_find_file", "project_switch_project",
      "send_buffer", "mu4e"]),
]


flatten_tree_pairs_cases = [
    # Test an empty dict
    ({}, []),
    # Test some single level "trees"
    ({"hello": "world",
      "one": 1,
      "two": 2, },
     [[["hello"], "world"],
      [["one"], 1],
      [["two"], 2]]),
    ({"tuple": (1, 2),
      "list": [1, 2],
      "dict": {1: 2},
      "int": 12, },
     [[["tuple"], (1, 2)],
      [["list"], [1, 2]],
      [["dict", 1], 2],
      [["int"], 12]]),
    # Test a tree with some light nesting
    ({"C-x": {"C-f": "find_file",
              "C-b": "switch_to_buffer",
              "C-c": "kill_ihmacs"},
      "C-f": "forward_char"},
     [[["C-x", "C-f"], "find_file"],
      [["C-x", "C-b"], "switch_to_buffer"],
      [["C-x", "C-c"], "kill_ihmacs"],
      [["C-f"], "forward_char"]]),
    # Test an incomplete tree, leaves are empty dicts
    ({"C-x": {},
      "C-f": "forward_char"},
     [[["C-f"], "forward_char"]]),
    # Test a large test tree
    (TEST_TREE_1,
     TEST_FLAT_TREE_PAIRS_1),
]


flatten_nested_list_cases = [
    # The empty list
    ([], []),
    # An already flat list
    ([1, 2, 3], [1, 2, 3]),
    (["this", "is", "a", "test", "case"],
     ["this", "is", "a", "test", "case"]),
    # 1 level of nesting
    ([[1], [2], [3]], [1, 2, 3]),
    ([["this"], "is", ["a", "test", "case"]],
     ["this", "is", "a", "test", "case"]),
    # Lots of nesting
    ([[[[[1, 2, 3, 4]], 5], 6, 7], [[[[8]], 9]]],
     [1, 2, 3, 4, 5, 6, 7, 8, 9]),
]


list_to_dict_cases = [
    # Length 2, this function requires that the list be at least 2 long
    ([1, 2], {1: 2}),
    (["a", "b"], {"a": "b"}),
    # Length 3:
    ([1, 2, 3], {1: {2: 3}}),
    (["a", "b", "c"], {"a": {"b": "c"}}),
    # Very long list
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     {0: {1: {2: {3: {4: {5: {6: {7: {8: 9}}}}}}}}}),
]


add_path_to_tree_cases = [
    # Add a path to an empty tree
    (["C-f", "forward_char"], {}, {"C-f": "forward_char"}),
    ([1, 2, 3], {}, {1: {2: 3}}),
    # Add a path to an existing tree.
    (["C-x", "C-f", "find_file"],
     {"C-f": "forward_char"},
     {"C-f": "forward_char",
      "C-x": {"C-f": "find_file"}}),
    # Overwrite an existing path
    ([1, 1],
     {1: "one",
      2: "two"},
     {1: 1,
      2: "two"}),
    # Add to a branching path
    ([1, 2, 3, 4],
     {1: {"hello": "world",
          "foo": "bar"}},
     {1: {"hello": "world",
          "foo": "bar",
          2: {3: 4}}}),
]


build_tree_from_pairs_cases = [
    # Test a single pair
    ([[["C-f"], "forward_char"]],
     {"C-f": "forward_char"}),
    # Test two pairs
    ([[["C-f"], "forward_char"],
      [["C-b"], "backward_char"]],
     {"C-f": "forward_char",
      "C-b": "backward_char"}),
    # Test a case where the same path shows up twice (should favor 2nd)
    ([[["C-f"], "forward_char"],
      [["C-f"], "foobar"]],
     {"C-f": "foobar"}),
    # Test a very large case, such as defining a default global keymap
    (TEST_FLAT_TREE_PAIRS_1,
     TEST_TREE_1),
]


replace_in_tree_cases = [
    # Test a case where no replacements are made
    ({1: "one",
      2: "two",
      3: {1: "thirty-one",
          2: "thirty-two"}},
     "three", "four",
     {1: "one",
      2: "two",
      3: {1: "thirty-one",
          2: "thirty-two"}}),
    # Test a case with a single replacement
    ({1: "one",
      2: "two",
      3: {1: "thirty-one",
          2: "thirty-two"}},
     "one", "five",
     {1: "five",
      2: "two",
      3: {1: "thirty-one",
          2: "thirty-two"}}),
    # Test a case with several replacements
    ({"C-f": "forward_char",
      "KEY_RIGHT": "forward_char",
      "C-b": "backward_char",
      "KEY_LEFT": "backward_char"},
     "forward_char", "foobar",
     {"C-f": "foobar",
      "KEY_RIGHT": "foobar",
      "C-b": "backward_char",
      "KEY_LEFT": "backward_char"}),
]


merge_trees_cases = [
    # Test a simple merge that is non-recursive
    ({1: "one",
      2: "two"},
     {3: "three",
      4: "four"},
     {1: "one",
      2: "two",
      3: "three",
      4: "four"}),
    # Test a recursive merge
    ({1: {1: "eleven",
          2: "twelve"},
      2: "two"},
     {1: {3: "thirteen"},
      3: "three"},
     {1: {1: "eleven",
          2: "twelve",
          3: "thirteen"},
      2: "two",
      3: "three"}),
    # Test a case with overwriting
    ({1: {1: "eleven",
          2: "twelve",
          3: "thirteen"},
      2: "two"},
     {1: "one",
      3: "three",
      4: {1: "forty-one",
          2: "forty-two"}},
     {1: "one",
      2: "two",
      3: "three",
      4: {1: "forty-one",
          2: "forty-two"}})
]


# Test functions for docstring_equal_p_cases

def test_func_1():
    """
    Identical docstring.
    """
    return 0


def test_func_2():
    """
    Identical docstring.
    """
    return 1


docstring_equal_p_cases = [
    # Test functions against itself and against other differing docstrings
    (tree_helpers.flatten_tree, tree_helpers.flatten_tree, True),
    (tree_helpers.flatten_tree, tree_helpers.flatten_tree_pairs, False),
    (tree_helpers.flatten_tree, tree_helpers.flatten_nested_list, False),
    (tree_helpers.flatten_tree, tree_helpers.list_to_dict, False),
    (tree_helpers.flatten_tree, tree_helpers.add_path_to_tree, False),
    (tree_helpers.flatten_tree, tree_helpers.replace_in_tree, False),
    (tree_helpers.flatten_tree, tree_helpers.merge_trees, False),
    (tree_helpers.flatten_tree, tree_helpers.docstring_equal_p, False),
    # Test differing functions with identical docstrings
    (test_func_1, test_func_2, True),
]


# Test functions
@pytest.mark.parametrize("tree,result", flatten_tree_cases)
def test_flatten_tree(tree, result):
    """
    Test that trees are correctly flattened.

    Args:
        tree: The dictionary tree to input to flatten_tree.
        result: The list representing the expected result.
    """
    returned_result = tree_helpers.flatten_tree(tree)
    assert returned_result == result


@pytest.mark.parametrize("tree,result", flatten_tree_pairs_cases)
def test_flatten_tree_pairs(tree, result):
    """
    Test that trees are correctly flattened into a path and a leaf.

    Args:
        tree: The dictionary tree to input to flatten_tree_pairs
        result: The list representing the expected result.
    """
    returned_result = tree_helpers.flatten_tree_pairs(tree)
    assert returned_result == result


@pytest.mark.parametrize("nested_list,result", flatten_nested_list_cases)
def test_flatten_nested_list(nested_list, result):
    """
    Test that a nested list is correctly flattened.

    Args:
        nested_list: A nested list to pass to flatten_nested_list.
        result: The list representing the expected result.
    """
    returned_result = tree_helpers.flatten_nested_list(nested_list)
    assert returned_result == result


@pytest.mark.parametrize("flat_list,result", list_to_dict_cases)
def test_list_to_dict(flat_list, result):
    """
    Test that a flat list is correctly turned into a dictionary.

    Args:
        flat_list: A flat list to pass to list_to_dict.
        result: The dictionary representing the expected result.
    """
    returned_result = tree_helpers.list_to_dict(flat_list)
    assert returned_result == result


@pytest.mark.parametrize("path,tree,result", add_path_to_tree_cases)
def test_add_path_to_tree(path, tree, result):
    """
    Test that a path is correctly added to a tree.

    Args:
        path: A list of hashables representing a path and a leaf to add to a
            tree.
        tree: A dictionary tree to add the path to.
        result: The dictionary tree representing the expected result.
    """
    returned_result = tree_helpers.add_path_to_tree(path, tree)
    assert returned_result == result


@pytest.mark.parametrize("flat_tree_pairs,result", build_tree_from_pairs_cases)
def test_build_tree_from_pairs(flat_tree_pairs, result):
    """
    Test that a list of pairs is correctly transformed into a dictionary tree.

    Args:
        flat_tree_pairs: A list of pairs, with each pair being a path and a
            leaf, to pass to build_tree_from_pairs.
        result: The dictionary tree representing the expected result.
    """
    returned_result = tree_helpers.build_tree_from_pairs(flat_tree_pairs)
    assert returned_result == result


@pytest.mark.parametrize("tree,item,replacement,result",
                         replace_in_tree_cases)
def test_replace_in_tree(tree, item, replacement, result):
    """
    Test that all instances of an item are replaced in a tree using the
    operator.eq comparison.

    Args:
        tree: The dictionary tree representing the original tree.
        item: An item in the tree to replace (any datatype).
        replacement: An item to replace with (any datatype).
        result: The dictionary tree representing the expected result.
    """
    returned_result = tree_helpers.replace_in_tree(tree, item, replacement)
    assert returned_result == result


@pytest.mark.parametrize("tree1,tree2,result", merge_trees_cases)
def test_merge_trees(tree1, tree2, result):
    """
    Test that two trees are correctly merged.

    Args:
        tree1: A dictionary tree.
        tree2: A dictionary tree.
        result: The dictionary tree representing the expected result of the
            merge.
    """
    returned_result = tree_helpers.merge_trees(tree1, tree2)
    assert returned_result == result


@pytest.mark.parametrize("func1,func2,result", docstring_equal_p_cases)
def test_docstring_equal_p(func1, func2, result):
    """
    Test is docstring comparison is correct.

    Args:
        func1: A function with a docstring.
        func2: A function with a docstring.
        result: A bool representing the comparison.
    """
    returned_result = tree_helpers.docstring_equal_p(func1, func2)
    assert returned_result == result
