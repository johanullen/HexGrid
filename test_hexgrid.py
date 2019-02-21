from unittest import TestCase
from unittest import main

from itertools import chain

from hexgrid import HexGrid

class TestHexGridBase(TestCase):

    def assertIsGrid(self, grid):
        self.assertIsInstance(grid, HexGrid)
        self.assertIsInstance(grid.grid, list)
        for row in grid.grid:
            self.assertIsInstance(row, list)
        self.assertIsInstance(grid.order, int)
        self.assertGreater(grid.order, 0)
        self.assertIsInstance(grid.height, int)
        self.assertGreaterEqual(grid.height, 0)
        self.assertIsInstance(grid.size, int)
        self.assertGreaterEqual(grid.size, 1)

    def assertGridIsNotGrid(self, actual, expected):
        self.assertIsNot(actual, expected)
        self.assertIsNot(actual.grid, expected.grid)
        for actual_row, expected_row in zip(actual.grid, expected.grid):
            self.assertIsNot(actual_row, expected_row)

    def assertGridAndListListEqual(self, test_grid, expected):
        self.assertIsGrid(test_grid)
        actual = test_grid.grid
        self.assertListEqual(actual, expected)
        self.assertEqual(test_grid.height, len(expected))
        self.assertEqual(test_grid.size, len(list(chain(*expected))))

    def assertGridEqual(self, actual_grid, expected_grid):
        self.assertEqual(actual_grid.order, expected_grid.order)
        actual = actual_grid
        expected = expected_grid.grid
        self.assertGridAndListListEqual(actual, expected)

    def test_from_order(self):
        self.assertGridAndListListEqual(HexGrid.from_order(1), expected=[[0]])
        self.assertGridAndListListEqual(HexGrid.from_order(2), expected=[[0, 0], [0, 0, 0], [0, 0]])
        self.assertGridAndListListEqual(HexGrid.from_order(3), expected=[[0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0]])

    def test_eq(self):
        actual = HexGrid.from_order(0)
        expected = HexGrid.from_order(0)
        self.assertEqual(actual, expected)

    def test_from_grid(self):
        actual = HexGrid.from_grid([[0]])
        expected = HexGrid.from_order(1)
        self.assertGridEqual(actual, expected)

    def test_copy(self):
        expected = HexGrid.from_order(3)
        with self.assertRaises(AssertionError):
            self.assertGridIsNotGrid(expected, expected)
        actual = expected.copy()
        self.assertGridEqual(actual, expected)
        self.assertGridIsNotGrid(actual, expected)

    def test_generator(self):
        expected = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 0),
            ((1, 2), 0),
            ((2, 0), 0),
            ((2, 1), 0),
        ]
        actual = list(HexGrid.from_order(2).generator())
        self.assertListEqual(actual, expected)

    def test_index_generator(self):
        expected = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
        ]
        actual = list(HexGrid.from_order(2).index_generator())
        self.assertListEqual(actual, expected)

    def test_index_generator(self):
        expected = [0]*7
        actual = list(HexGrid.from_order(2).value_generator())
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    main(verbosity=2)