# Copyright 2017 Chris Cartland. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

class BST(object):
  """Binary Search Tree class.

  Supports insert(), find() and delete() operations."""

  def __init__(self):
    self.root = None

  def __str__(self):
    return str(self.root)

  def insert(self, item):
    """Inserts an item into the binary search tree.

    Args:
      item: A value that can be compared to other values in the tree.

    Returns:
      None
    """
    node = BinaryTreeNode(item)
    self.root = BST.insert_node(self.root, node)

  @staticmethod
  def insert_node(root, new_node):
    """Insert a node into the tree at root.

    Args:
      root: Existing node in the tree. Can be None.
      new_node: The node to be inserted into the tree. Can be None.

    Returns:
      The modified root node.
    """
    if new_node is None:
      return root
    if root is None:
      return new_node

    node = root
    while node is not None:
      if node.datum < new_node.datum:
        if node.right is None:
          node.right = new_node
          return root
        node = node.right
      else:
        if node.left is None:
          node.left = new_node
          return root
        node = node.left
    raise ValueError('Something went wrong')

  def find(self, item):
    """Returns BinaryTreeNode that matches the item, or None if it does not exist.

    Args:
      item: A value that can be compared to other values in the tree.

    Returns:
      The BinaryTreeNode or None.
    """
    node = self.root
    if node is None:
      return None

    while node is not None:
      if node.datum == item:
        return node
      elif node.datum < item:
        node = node.right
      elif item < node.datum:
        node = node.left
      else:
        raise ValueError('Something went wrong')
    return None

  def delete(self, item):
    """Delete a single node that matches item. No effect if the item does not exist.

    Args:
      item: A value that can be compared to other values in the tree.

    Returns:
      None
    """
    self.root = BST.delete_item(self.root, item)

  @staticmethod
  def delete_item(root, item):
    """Delete a single node from the root, and return the modified root.

    The original root is returned if the item is not found.

    Args:
      root: Existing node in the tree. Can be None.
      item: A value that can be compared to other values in the tree.

    Returns:
      The modified root node.
    """
    if root is None:
      return None

    parent = None
    node = root
    while node.datum != item:
      if node.datum < item:
        parent = node
        node = node.right
      elif item < node.datum:
        parent = node
        node = node.left
      if node is None:
        # BST did not contain item.
        return root

    left = node.left
    right = node.right
    if parent is not None:
      if item < parent.datum:
        parent.left = None
      if parent.datum < item:
        parent.right = None
    node_is_root = (parent is None)
    parent = BST.insert_node(parent, right)
    parent = BST.insert_node(parent, left)
    if node_is_root:
      root = parent
    return root

  def is_valid(self):
    """Validate the binary search tree.

    For every node:
    1) The left branch must only contain nodes with lesser or equal value
    2) The right branch must only contain nodes with greater or equal value

    Returns:
      True if this is a valid binary search tree.
    """
    return BST.is_valid_node(self.root, mn=None, mx=None)

  @staticmethod
  def is_valid_node(node, mn, mx):
    """Validate the node for a binary search tree.

    Args:
			node: The current node.
      mn: The minimum value for this node and subnodes. None if no min is set.
      mx: The maximum value for this node and subnodes. None if no max is set.

    Returns:
      True if this node and all subnodes are valid binary search tree nodes.
    """
    if node is None:
      return True

    if mn is not None and node.datum < mn:
        return False
    if mx is not None and node.datum > mx:
        return False
    if not BST.is_valid_node(node.left, mn, node.datum):
      return False
    if not BST.is_valid_node(node.right, node.datum, mx):
      return False
    return True


class BinaryTreeNode(object):
  """A binary tree node contains a datum nd two children.

  Attributes:
    datum: A value that can be compared to other values in the tree.
    left: The BinaryTreeNode for the left branch.
    right: the BinaryTreeNode for the right branch.
  """

  def __init__(self, datum):
    self.datum = datum
    self.left = None
    self.right = None

  def __str__(self):
    return self.pretty_str()

  def pretty_str(self, indent=0):
    """Human readable view of the tree.

    Args:
      self: BinaryTreeNode.
      indent: The number of spaces that this node needs to be indented.

    Returns:
      A string that can be printed to the command line."""
    output = ''
    if self.right is not None:
      output += self.right.pretty_str(indent+2)
      output += '\n'
      output += ' ' * indent
      output += ' /'
      output += '\n'
    output += ' ' * indent
    output += str(self.datum)
    if self.left is not None:
      output += '\n'
      output += ' ' * indent
      output += ' \\\n'
      output += self.left.pretty_str(indent+2)
    return output


class TestBST(unittest.TestCase):
  """Test cases for the BST."""

  def test_empty(self):
    bst = BST()
    self.assertIsNotNone(bst)
    self.assertTrue(bst.is_valid())

  def test_insert_and_find(self):
    bst = BST()
    bst.insert(1)
    result = bst.find(1)
    self.assertEqual(result.datum, 1)
    self.assertTrue(bst.is_valid())

  def test_find_item_that_does_not_exist(self):
    bst = BST()
    bst.insert(2)
    bst.insert(3)
    result = bst.find(4)
    self.assertIsNone(result)
    self.assertTrue(bst.is_valid())

  def test_delete_item(self):
    bst = BST()
    bst.insert(5)
    result = bst.find(5)
    self.assertIsNotNone(result)
    bst.delete(5)
    result = bst.find(5)
    self.assertIsNone(result)
    self.assertTrue(bst.is_valid())

  def test_delete_leaf_right(self):
    bst = BST()
    bst.insert(8)
    bst.insert(6)
    bst.insert(7)

    result = bst.find(7)
    self.assertIsNotNone(result)
    bst.delete(7)
    result = bst.find(7)
    self.assertIsNone(result)
    self.assertTrue(bst.is_valid())

  def test_delete_leaf_left(self):
    bst = BST()
    bst.insert(9)
    bst.insert(11)
    bst.insert(10)

    result = bst.find(10)
    self.assertIsNotNone(result)
    bst.delete(10)
    result = bst.find(10)
    self.assertIsNone(result)
    self.assertTrue(bst.is_valid())

  def test_delete_root_full(self):
    bst = BST()
    bst.insert(13)
    bst.insert(12)
    bst.insert(14)

    result = bst.find(13)
    self.assertIsNotNone(result)
    bst.delete(13)
    result = bst.find(13)
    self.assertIsNone(result)
    self.assertTrue(bst.is_valid())


if __name__ == '__main__':
  unittest.main()

