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

class Heap(object):
  """Min/max heap implementation.

  Min heap by default. Use Heap(max_heap=True) to create a max heap.

  Items are inserted with Heap.insert().
  The top item can be viewed with Heap.peek().
  The top item can be removed with Heap.pop().
  """

  def __init__(self, max_heap=False):
    self.items = [None] # Index 0 is unused for easier math.
    self.item_count = 0
    self.invalid_index_set = set()
    self.is_max_heap = max_heap

  def __str__(self):
    return 'Count: %d, Items: %s, Invalid Index Set: %s' % (self.count(),
        str(self.items), self.invalid_index_set)

  def count(self):
    return self.item_count

  def is_heap_order(self, parent, child):
    if self.is_max_heap:
      # Max heap.
      return parent >= child
    else:
      # Min heap.
      return parent <= child

  def insert(self, item):
    """Insert an item into the min heap.

    Args:
      item: A value that can be compared to other values in the heap.

    Returns:
      None

    Runtime:
      O(log(N)) time where N is the number of items in the heap.
    """
    index = self.insert_at_next_index(item)
    self.items[index] = item
    while index > 1:
      parent_index = index / 2 # Truncate, e.g. 4 and 5 have parent 2.
      if self.is_heap_order(self.items[parent_index], self.items[index]):
        # The item does not need to bubble up anymore. Done.
        return
      else:
        # Swap items at index and parent_index
        temp = self.items[index]
        self.items[index] = self.items[parent_index]
        self.items[parent_index] = temp
        index = parent_index
    # The item bubbled all the way to the root. Done.
    return

  def insert_at_next_index(self, item):
    self.item_count += 1
    if len(self.invalid_index_set) == 0:
      # Return index for a new item in the list.
      index = len(self.items)
      self.items.append(item)
      return index
    index = self.invalid_index_set.pop()
    self.items[index] = item
    return index

  def peek(self):
    """Peek at the top item in the heap.

    Returns:
      The top item.

    Runtime:
      Constant time O(1).
    """
    if self.count() <= 0:
      raise ValueError('Cannot peek at value that does not exist')
    return self.items[1]

  def pop(self):
    """Remove and return the top item.

    Returns:
      The top item.

    Runtime:
      O(log(N)) time where N is the number of items in the heap.
    """
    result = self.peek()
    self.item_count -= 1
    index = 1
    mem_size = len(self.items)
    while True:
      left = index * 2
      right = left + 1
      if self.is_invalid_index(left) and self.is_invalid_index(right):
        # Neither child exists, so delete this item.
        self.mark_invalid_index(index)
        return result
      elif self.is_invalid_index(right):
        # Right child does not exist, so bubble up from left.
        self.items[index] = self.items[left]
        index = left
      elif self.is_invalid_index(left):
        # Left child does not exist, so bubble up from right.
        self.items[index] = self.items[right]
        index = right
      elif self.is_heap_order(self.items[left], self.items[right]):
        # Left child should be on top, so bubble up from left.
        self.items[index] = self.items[left]
        index = left
      else:
        # Right child should be on top, so bubble up from right.
        self.items[index] = self.items[right]
        index = right

  def is_invalid_index(self, index):
    if index <= 0:
      return True
    if index >= len(self.items):
      return True
    return index in self.invalid_index_set

  def mark_invalid_index(self, index):
    self.invalid_index_set.add(index)


class TestHeap(unittest.TestCase):
  """Test cases for the min-heap."""

  def test_empty(self):
    heap = Heap()
    self.assertIsNotNone(heap)

  def test_insert_one(self):
    heap = Heap()
    heap.insert(1)
    result = heap.peek()
    self.assertEqual(result, 1)

  def test_insert_two(self):
    heap = Heap()
    heap.insert(2)
    heap.insert(1)
    result = heap.peek()
    self.assertEqual(result, 1)

  def test_pop(self):
    heap = Heap()
    heap.insert(5)
    heap.insert(1)
    heap.insert(2)
    heap.insert(4)
    heap.insert(3)
    result = heap.pop()
    self.assertEqual(result, 1)
    result = heap.pop()
    self.assertEqual(result, 2)
    result = heap.pop()
    self.assertEqual(result, 3)
    result = heap.pop()
    self.assertEqual(result, 4)
    result = heap.pop()
    self.assertEqual(result, 5)

  def test_pop_and_insert(self):
    heap = Heap()
    heap.insert(7)
    heap.insert(6)
    result = heap.pop()
    self.assertEqual(result, 6)
    heap.insert(8)
    result = heap.pop()
    self.assertEqual(result, 7)

  def test_max_heap(self):
    heap = Heap(max_heap=True)
    heap.insert(7)
    heap.insert(6)
    result = heap.pop()
    self.assertEqual(result, 7)
    heap.insert(8)
    result = heap.pop()
    self.assertEqual(result, 8)


if __name__ == '__main__':
  unittest.main()

