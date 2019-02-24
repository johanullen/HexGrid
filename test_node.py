from unittest import TestCase
from unittest import main

from node import Node

class TestNode(TestCase):
    def setUp(self):
        self.node0 = Node(0)
        self.node1 = Node(1)
        self._node1 = Node(1)
        self.node2 = Node(2)

        self.int0 = 0
        self.int1 = 1
        self.int2 = 2

    def test_eq(self):
        self.assertTrue(self.node1 == self.node1)
        self.assertTrue(self.node1 == self._node1)
        self.assertFalse(self.node1 == self.node2)
        self.assertTrue(self.node1 == self.int1)
        self.assertFalse(self.node1 == self.int2)

    def test_ne(self):
        self.assertFalse(self.node1 != self.node1)
        self.assertFalse(self.node1 != self._node1)
        self.assertTrue(self.node1 != self.node2)
        self.assertFalse(self.node1 != self.int1)
        self.assertTrue(self.node1 != self.int2)

    def test_lt(self):
        self.assertFalse(self.node1 < self.node0)
        self.assertFalse(self.node1 < self.node1)
        self.assertFalse(self.node1 < self._node1)
        self.assertTrue(self.node1 < self.node2)
        self.assertFalse(self.node1 < self.int0)
        self.assertFalse(self.node1 < self.int1)
        self.assertTrue(self.node1 < self.int2)

    def test_le(self):
        self.assertFalse(self.node1 <= self.node0)
        self.assertTrue(self.node1 <= self.node1)
        self.assertTrue(self.node1 <= self._node1)
        self.assertTrue(self.node1 <= self.node2)
        self.assertFalse(self.node1 <= self.int0)
        self.assertTrue(self.node1 <= self.int1)
        self.assertTrue(self.node1 <= self.int2)

    def test_gt(self):
        self.assertTrue(self.node1 > self.node0)
        self.assertFalse(self.node1 > self.node1)
        self.assertFalse(self.node1 > self._node1)
        self.assertFalse(self.node1 > self.node2)
        self.assertTrue(self.node1 > self.int0)
        self.assertFalse(self.node1 > self.int1)
        self.assertFalse(self.node1 > self.int2)

    def test_ge(self):
        self.assertTrue(self.node1 >= self.node0)
        self.assertTrue(self.node1 >= self.node1)
        self.assertTrue(self.node1 >= self._node1)
        self.assertFalse(self.node1 >= self.node2)
        self.assertTrue(self.node1 >= self.int0)
        self.assertTrue(self.node1 >= self.int1)
        self.assertFalse(self.node1 >= self.int2)


    def test_neg(self):
        actual = -self.node1
        expected = Node(-1)
        self.assertEqual(actual, expected)

    def test_add(self):
        expected = Node(3)
        actual = self.node1 + self.node2
        self.assertEqual(actual, expected)
        actual = self.node1 + self.int2
        self.assertEqual(actual, expected)

    def test_sub(self):
        expected = Node(-1)
        actual = self.node1 - self.node2
        self.assertEqual(actual, expected)
        actual = self.node1 - self.int2
        self.assertEqual(actual, expected)

    def test_iadd(self):
        expected = Node(3)
        actual = Node(1)
        actual += self.node2
        self.assertEqual(actual, expected)
        expected = Node(5)
        actual += self.int2
        self.assertEqual(actual, expected)

    def test_isub(self):
        expected = Node(-1)
        actual = Node(1)
        actual -= self.node2
        self.assertEqual(actual, expected)
        expected = Node(-3)
        actual -= self.int2
        self.assertEqual(actual, expected)

    def test_index(self):
        l = [1, 2, 3]
        actual = l[self.node1]
        expected = 2
        self.assertEqual(actual, expected)

    def test_hash(self):
        expected = hash(self.node1)
        actual = hash(self.node1)
        self.assertEqual(actual, expected)
        actual = hash(self._node1)
        self.assertEqual(actual, expected)
        actual = hash(self.node2)
        self.assertNotEqual(actual, expected)
        actual = hash(self.node1)
        self.assertEqual(actual, expected)

    def test_str(self):
        expected = "1"
        actual = str(self.node1)
        self.assertEqual(actual, expected)
        actual = f"{self.node1}"
        self.assertEqual(actual, expected)
        actual = "%s" % self.node1
        self.assertEqual(actual, expected)
        actual = "%r" % self.node1
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    main(verbosity=2)