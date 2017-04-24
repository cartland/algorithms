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

import random
import sys
import unittest

from heap import Heap

class Sorter(object):

  def sort(self, data):
    raise NotImplementedError()

  def is_sorted(self, data):
    l = len(data)
    if l == 0:
      return True
    val = data[0]
    for i in xrange(1, len(data)):
      next_val = data[i]
      if val > next_val:
        return False
      val = next_val
    return True


class BubbleSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    done = False
    while not done:
      done = True
      for i in xrange(len(data) - 1):
        if data[i] > data[i+1]:
          temp = data[i]
          data[i] = data[i+1]
          data[i+1] = temp
          done = False
    return data


class HeapSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    heap = Heap()
    for d in data:
      heap.insert(d)
    for i in xrange(len(data)):
      data[i] = heap.pop()
    return data


class InsertionSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    for i in xrange(1, len(data)):
      for j in xrange(i, 0, -1):
        if data[j] < data[j-1]:
          temp = data[j-1]
          data[j-1] = data[j]
          data[j] = temp
    return data


class MergeSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    self.merge_sort(data, 0, len(data_input) - 1)
    return data

  def merge_sort(self, data, left, right):
    if left < right:
      center = (left + right) / 2
      self.merge_sort(data, left, center)
      self.merge_sort(data, center+1, right)
      self.merge(data, left, center+1, right)

  def merge(self, data, left, right, right_end):
    left_end = right - 1
    temp = []
    li = left
    ri = right
    while li <= left_end and ri <= right_end:
      if data[li] < data[ri]:
        temp.append(data[li])
        li += 1
      else:
        temp.append(data[ri])
        ri+= 1

    while li <= left_end:
      temp.append(data[li])
      li += 1

    while ri <= right_end:
      temp.append(data[ri])
      ri += 1

    for i in xrange(len(temp)):
      data[left + i] = temp[i]


class SelectionSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    for i in xrange(len(data)):
      best_index = i
      best_val = data[i]
      for j in xrange(i, len(data)):
        val = data[j]
        if val < best_val:
          best_index = j
          best_val = val
      temp = data[i]
      data[i] = data[best_index]
      data[best_index] = temp
    return data


class QuickSorter(Sorter):

  def sort(self, data_input):
    data = list(data_input) # Copy list
    self.quick_sort(data, 0, len(data) - 1)
    return data

  def quick_sort(self, data, lo, hi):
    if lo >= hi:
      return
    pivot = random.randint(lo, hi)
    pivot_val = data[pivot]
    data[pivot] = data[lo]
    data[lo] = pivot_val
    pivot = lo

    for i in xrange(lo, hi + 1):
      if data[i] < pivot_val:
        data[pivot] = data[i] # New value moves to pivot location
        data[i] = data[pivot + 1] # pivot+1 goes to new value's location
        data[pivot + 1] = pivot_val # pivot goes to pivot+1
        pivot += 1
    self.quick_sort(data, lo, pivot - 1)
    self.quick_sort(data, pivot + 1, hi)


class TestBubbleSorter(unittest.TestCase):
  """Test cases for sorters."""

  def setUp(self):
    self.data = test_data()

  def test_empty(self):
    sorter = BubbleSorter()
    data = []
    result = sorter.sort(data)
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_bubble_sort(self):
    sorter = BubbleSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Bubble Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_merge_sort(self):
    sorter = MergeSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Merge Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_heap_sort(self):
    sorter = HeapSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Heap Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_insertion_sort(self):
    sorter = InsertionSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Insertion Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_quick_sort(self):
    sorter = QuickSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Quick Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))

  def test_selection_sort(self):
    sorter = SelectionSorter()
    data = self.data
    result = sorter.sort(data)
    print 'Selection Sort'
    print result
    self.assertIsNotNone(result)
    self.assertEqual(len(result), len(data))
    self.assertTrue(sorter.is_sorted(result))


DATA = None
def test_data():
  global DATA
  if DATA is None:
    max_int = 100 # sys.maxint
    DATA = tuple(random.randint(0, max_int) for _ in xrange(30))
  return DATA


if __name__ == '__main__':
  unittest.main()

