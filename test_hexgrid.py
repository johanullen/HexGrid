from unittest import TestCase
from unittest import main

from itertools import chain

from hexgrid import HexGrid

class TestHexGridBase(TestCase):
    longMessage=True

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
        self.assertEqual(len(test_grid), len(list(chain(*expected))), msg=f"{expected}")

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

    def test_iter(self):
        expected = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 0),
            ((1, 2), 0),
            ((2, 0), 0),
            ((2, 1), 0),
        ]
        actual = list(HexGrid.from_order(2))
        self.assertListEqual(actual, expected)

    def test_len(self):
        actual = len(HexGrid.from_order(3))
        expected = 19
        self.assertEqual(actual, expected)


class TestHexGridManipulate(TestHexGridBase):
    
    def test_str_from_index_or_slice(self):
        test_cases = [
            (HexGrid._str_from_index_or_slice(1), "1"),
            (HexGrid._str_from_index_or_slice(slice(1, None)), "1::"),
            (HexGrid._str_from_index_or_slice(slice(3)), ":3:"),
            (HexGrid._str_from_index_or_slice(slice(0, 3)), "0:3:"),
            (HexGrid._str_from_index_or_slice(slice(1, 3, 1)), "1:3:1"),
            (HexGrid._str_from_index_or_slice(slice(None, None, 2)), "::2"),
        ]
        for actual, expected in test_cases:
            self.assertIsInstance(actual, str)
            self.assertEqual(actual, expected)

        with self.assertRaises(TypeError):
            HexGrid._str_from_index_or_slice("1")

    def test_error_check_index(self):
        height = 3
        int_cases = list(range(0, height))
        {HexGrid._error_check_index(index, height) for index in int_cases}
        slice_cases = list()
        for start in list(range(0, height)) + [None]:
            slice_cases.append(slice(start))
            for stop in list(range(start or 0, height)) + [None]:
                for step in [None, 1]:
                    slice_cases.append(slice(start, stop, step))
        {HexGrid._error_check_index(index, height) for index in slice_cases}

        index_error_cases = [
            (-1, height),
            (3, height),
            (slice(4), height),
            (slice(-1, 2), height),
            (slice(1, 4), height),
            (slice(1, 2, 2), height),
        ]
        type_error_cases = ["1", 1.5, (1, 2)]

        def assertRaises(index, height, error):
            with self.assertRaises(error, msg=f"{error} not raised index={index}, height={height}"):
                HexGrid._error_check_index(index, height)
        {assertRaises(index, height, IndexError) for index, height in index_error_cases}
        {assertRaises(index, 10, TypeError) for index in index_error_cases}

    def test_error_check_getitem(self):
        hexgrid = HexGrid.from_order(3)
        correct_cases = [
            (1, ("index", 1)),
            (slice(0, 2), ("index", slice(0, 2))),
            ((1,), ("index", 1)),
            ((slice(0, 2), 0), ("indices", slice(0, 2), 0)),
            ((1, slice(0, 2)), ("indices", 1, slice(0, 2))),
            ((slice(0, 2), slice(0, 2)), ("indices", slice(0, 2), slice(0, 2))),
            (("list", 0, 2), ("list", 0, 2, 1)),
            (("list", 0, 2, 1), ("list", 0, 2, 1)),
            (("LIST", 0, 2), ("list", 0, 2, 1)),
            (("grid", 0, 2), ("grid", 0, 2, 1)),
            (("grid", 0, 2, 1), ("grid", 0, 2, 1)),
            (("GRID", 0, 2), ("grid", 0, 2, 1)),
        ]
        for index, expected in correct_cases:
            actual = hexgrid._error_check_getitem(index)
            self.assertTupleEqual(actual, expected)

        incorrect_cases = [
            ((1, 0, 2), TypeError),
            (("lists", 0, 2), ValueError),
            (("list", 0, 2, 1, 2), TypeError),
        ]
        def assertRaises(index, error):
            with self.assertRaises(error, msg=f"{error} not raised index={index}"):
                hexgrid._error_check_getitem(index)
        {assertRaises(index, error) for index, error in incorrect_cases}

    def test_getitem(self):
        grid = [
            [4, 3, 2],
            [2, 1, 3, 1],
            [3, 1, 5, 2, 4],
            [2, 1, 4, 3],
            [2, 3, 1],
        ]
        hexgrid = HexGrid.from_grid(grid)

        actual = hexgrid[0]
        expected = grid[0]
        self.assertListEqual(actual, expected)

        actual = hexgrid[0:2]
        expected = grid[0:2]
        self.assertListEqual(actual, expected)

        actual = hexgrid[0, 0]
        expected = grid[0][0]
        self.assertEqual(actual, expected)

        actual = hexgrid[0, 0:2]
        expected = grid[0][0:2]
        self.assertListEqual(actual, expected)

        actual = hexgrid[0:2, 0:2]
        expected = [[4, 3], [2, 1]]
        self.assertListEqual(actual, expected)

        actual = hexgrid["list", 2, 2]
        expected = [
            [1, 3],
            [1, 5, 2],
            [1, 4],
        ]
        self.assertListEqual(actual, expected)

        actual = hexgrid["list", 2, 2, 2]
        expected = grid
        self.assertListEqual(actual, expected)

        actual = hexgrid["grid", 2, 2]
        self.assertIsGrid(actual)
        expected_grid = [
            [1, 3],
            [1, 5, 2],
            [1, 4],
        ]
        expected = HexGrid.from_grid(expected_grid)
        self.assertGridEqual(actual, expected)

        actual = hexgrid["grid", 2, 2, 2]
        self.assertIsGrid(actual)
        expected = HexGrid.from_grid(grid)
        self.assertGridEqual(actual, expected)


if __name__ == '__main__':
    main(verbosity=2)