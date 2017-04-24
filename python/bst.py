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

from bt import BinaryTreeNode
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

  def balance(self):
    """Balance the BST to reduce the tree's depth.

    Preserves the BST ordering by performing tree rotations.

    Returns:
      None
    """
    self.root = BST.balance_node(self.root)

  @staticmethod
  def balance_node(node):
    """Balance this node and return the new root."""
    if node is None:
      return None
    balancing = True
    while balancing:
      balancing = False
      node.left = BST.balance_node(node.left)
      node.right = BST.balance_node(node.right)
      left_depth = BST.node_depth(node.left)
      right_depth = BST.node_depth(node.right)
      if left_depth >= right_depth+2:
        outside_depth = BST.node_depth(node.left.left)
        inside_depth = BST.node_depth(node.left.right)
        if inside_depth > outside_depth:
          # If the inner branch is deeper, then
          # rotating will not help balance the depth.
          pass
        else:
          node = BST.rotate_right(node)
          balancing = True
      elif right_depth >= left_depth+2:
        outside_depth = BST.node_depth(node.right.right)
        inside_depth = BST.node_depth(node.right.left)
        if inside_depth > outside_depth:
          # If the inner branch is deeper, then
          # rotating will not help balance the depth.
          pass
        else:
          node = BST.rotate_left(node)
          balancing = True
    return node

  @staticmethod
  def rotate_left(node):
    if node is None:
      return None
    if node.right is None:
      # Cannot rotate left if right branch does not exist.
      return node
    new_root = node.right
    orphan = new_root.left
    new_root.left = node
    node.right = orphan
    return new_root

  @staticmethod
  def rotate_right(node):
    if node is None:
      return None
    if node.left is None:
      # Cannot rotate right if left branch does not exist.
      return node
    new_root = node.left
    orphan = new_root.right
    new_root.right= node
    node.left= orphan
    return new_root

  def depth(self):
    """Return the depth of the BST.

    Returns:
      Empty tree returns 0.
      Tree with a single node returns 1.
      Returns 1 + the max depth of the left and right branches.
    """
    return BST.node_depth(self.root)

  @staticmethod
  def node_depth(node):
    if node is None:
      return 0
    left = BST.node_depth(node.left)
    right = BST.node_depth(node.right)
    return 1 + max(left, right)

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

  def test_depth(self):
    bst = BST()
    bst.insert(15)
    bst.insert(16)
    bst.insert(17)
    self.assertEqual(bst.depth(), 3)

  def test_balance(self):
    bst = BST()
    bst.insert(18)
    bst.insert(19)
    bst.insert(20)
    bst.insert(21)
    bst.insert(22)
    bst.insert(23)
    self.assertEqual(bst.depth(), 6)
    bst.balance()
    self.assertEqual(bst.depth(), 4)

  def test_stable(self):
    """Do not balance a tree that cannot be balanced."""
    bst = BST()
    bst.insert(18)
    bst.insert(20)
    bst.insert(19)
    self.assertEqual(bst.depth(), 3)
    bst.balance()
    self.assertEqual(bst.depth(), 3)


if __name__ == '__main__':
  unittest.main()

