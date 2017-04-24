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
    output += '-' + str(self.datum)
    if self.left is not None:
      output += '\n'
      output += ' ' * indent
      output += ' \\\n'
      output += self.left.pretty_str(indent+2)
    return output


class TestBTN(unittest.TestCase):
  """Test cases for the binary tree node."""

  def test_single_node(self):
    node = BinaryTreeNode(1)
    print
    print str(node)
    self.assertIsNotNone(node)
    self.assertIsNone(node.left)
    self.assertIsNone(node.right)
    self.assertEqual(node.datum, 1)

  def test_left(self):
    node = BinaryTreeNode('Root Node')
    node.left = BinaryTreeNode('Left Node')
    print
    print str(node)
    self.assertEqual(node.left.datum, 'Left Node')

  def test_right(self):
    node = BinaryTreeNode('Root Node')
    node.right= BinaryTreeNode('Right Node')
    print
    print str(node)
    self.assertEqual(node.right.datum, 'Right Node')

  def test_both(self):
    node = BinaryTreeNode('Root Node')
    node.left = BinaryTreeNode(0)
    node.right = BinaryTreeNode(True)
    print
    print str(node)
    self.assertEqual(node.datum, 'Root Node')
    self.assertEqual(node.left.datum, 0)
    self.assertEqual(node.right.datum, True)


if __name__ == '__main__':
  unittest.main()
