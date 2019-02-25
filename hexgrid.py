import random
from multiprocessing import Process, Manager, Lock
from itertools import chain, groupby, starmap
from collections import Counter
from functools import reduce

from node import Node


class HexGridBase:

    def __init__(self, grid, order, height, size, *, NodeType=Node):
        self.order = order
        self.height = height
        self.size = size
        self.grid = [list(row) for row in grid]
        for (x, y), value in self.generator():
            self.grid[x][y] = Node(value)

    def copy(self):
        new_grid = list()
        for row in self.grid:
            new_grid.append(row.copy())
        return type(self)(
            new_grid,
            self.order,
            self.height,
            self.size,
        )

    @classmethod
    def from_order(cls, order=3):
        width = order
        grid = list()
        while width <= 2*order-1:
            grid.append([0]*width)
            width += 1
        width -= 1
        while width > order:
            width -= 1
            grid.append([0]*width)

        height = len(grid)
        size = 3 * order**2 - 3 * order + 1
        return cls(grid, order, height, size)

    @classmethod
    def from_grid(cls, grid):
        order = len(grid[0])
        height = len(grid)
        size = 3 * order**2 - 3 * order + 1
        return cls(grid, order, height, size)

    def generator(self):
        for x, row in enumerate(self.grid):
            for y, val in enumerate(row):
                yield (x, y), val

    def index_generator(self):
        for coords, _ in self.generator():
            yield coords

    def value_generator(self):
        for _, value in self.generator():
            yield value

    def __iter__(self):
        return self.generator()

    def __len__(self):
        return self.size

    def __eq__(self, other):
        if self.order != other.order:
            return False
        if self.height != other.height:
            return False
        if self.size != other.size:
            return False
        for s, o in zip(chain(*self.grid), chain(*other.grid)):
            if s != o:
                return False
        return True


class HexGridManipulate(HexGridBase):

    @staticmethod
    def _str_from_index_or_slice(index):
        if isinstance(index, int):
            return f"{index}"
        elif isinstance(index, slice):
            start = index.start
            stop = index.stop
            step = index.step
            if start is None:
                start = ""
            else:
                start = f"{start}"
            if stop is None:
                stop = ""
            else:
                stop = f"{stop}"
            if step is None:
                step = ""
            else:
                step = f"{step}"
            return f"{start}:{stop}:{step}"
        else:
            raise TypeError(f"index must be integer or slice, not {type(index)}")

    @staticmethod
    def _error_check_index(index, height, *, name="", prefix="", suffix="", allow_slice=True):
        if isinstance(index, int):
            if index < 0:
                raise IndexError(f"grid[{prefix}{name}{suffix}] index out of range: {index} < 0")
            if index >= height:
                raise IndexError(f"grid[{prefix}{name}{suffix}] index out of range: {index} >= {height}")
        elif allow_slice and isinstance(index, slice):
            if index.start is not None and index.start < 0:
                raise IndexError(f"grid[{prefix}{name}.start:] index out of range: {index.start} < 0")
            if index.stop is not None and index.stop > height:
                raise IndexError(f"grid[{prefix}:{name}.stop] index out of range: {index.stop} > {height}")
            if index.step not in (None, 1):
                raise IndexError(f"grid[{prefix}::{name}.step] index must be None or 1: {index.step} not in (None, 1)")
        elif allow_slice:
            raise TypeError(f"grid[{prefix}{name}{suffix}] index must be integer or slice, not {type(index)}")
        else:
            raise TypeError(f"grid[{prefix}{name}{suffix}] index must be integer, not {type(index)}")

    def _error_check_getitem(self, index):
        if isinstance(index, (int, slice)) or isinstance(index, tuple) and len(index)==1:
            if isinstance(index, tuple):
                index = index[0]
            self._error_check_index(index, self.height, name="x")
            return "index", index

        if isinstance(index, tuple) and len(index)==2:
            x, y = index
            self._error_check_index(x, self.height, name="x")
            if isinstance(x, int):
                height = len(self.grid[x])
            else:
                height = min(map(len, self.grid[x]))
            prefix = self._str_from_index_or_slice(x)
            self._error_check_index(y, height, name="y", prefix="{prefix}, ")
            return "indices", x, y

        if isinstance(index, tuple) and len(index) in (3, 4):
            if len(index)==3:
                slice_type, x, y = index
                size = 1
            else:
                slice_type, x, y, size = index
            if not isinstance(slice_type, str):
                raise TypeError(f"slice_type must be string, not {type(slice_type)}")
            slice_type = slice_type.lower()
            if slice_type not in ("list", "grid"):
                raise ValueError(f"slice_type must be either \"list\" or \"grid\", not {slice_type}")
            self._error_check_index(x, self.height, name="x", prefix=slice_type+", ", suffix=", y, [size]", allow_slice=False)
            height = len(self.grid[x])
            self._error_check_index(y, self.height, name="y", prefix=slice_type+", z, ", suffix=", [size]", allow_slice=False)
            return slice_type, x, y, size

        raise TypeError(f"""
            indices must be integer; slices; 2-tuples of integer or slizes;
            or 3/4-tuples like "list"/"grid", x, y, [size]; not {type(index)}""")

    def __getitem__(self, index):
        index = self._error_check_getitem(index)
        slice_type = index[0]
        if slice_type == "index":
            x = index[1]
            return self.grid[x]
        if slice_type == "indices":
            x, y = index[1:]
            if isinstance(x, int):
                return self.grid[x][y]
            slices = list()
            for row in self.grid[x]:
                slices.append(row[y])
            return slices
        if slice_type in ("list", "grid"):
            x, y, size = index[1:]
            rows = self._apply_at_dist(
                (x, y),
                lambda _x, _y: (_x, _y),
                lambda ret: chain(*ret),
                size,
            )
            rows = sorted(rows)
            row_groups = groupby(rows, lambda x: x[0])

            def min_and_max(row):
                _, ys = zip(*row)
                ys = list(ys)
                min_y = min(ys)
                max_y = max(ys)
                return min_y, max_y
            row_ranges = starmap(lambda x, row: (x, min_and_max(row)), row_groups)
            row_ranges = sorted(row_ranges)
            grid = list()
            for x, (start, stop) in row_ranges:
                grid.append(self[x, start:stop+1])
            if slice_type == "list":
                return grid
            if slice_type == "grid":
                return self.from_grid(grid)

    def _apply(self, node, apply_func, *, default=None):
        x, y = node

        def f(_x, _y):
            if self._no_index_error(_x, _y):
                return apply_func(_x, _y)
            else:
                return default
        ret_list = list()
        if x < self.order-1:
            ret_list.append(f(x-1, y-1))
            ret_list.append(f(x-1, y))
            ret_list.append(f(x, y-1))
            ret_list.append(f(x, y+1))
            ret_list.append(f(x+1, y))
            ret_list.append(f(x+1, y+1))
        elif x > self.order-1:
            ret_list.append(f(x-1, y))
            ret_list.append(f(x-1, y+1))
            ret_list.append(f(x, y-1))
            ret_list.append(f(x, y+1))
            ret_list.append(f(x+1, y-1))
            ret_list.append(f(x+1, y))
        else:
            ret_list.append(f(x-1, y-1))
            ret_list.append(f(x-1, y))
            ret_list.append(f(x, y-1))
            ret_list.append(f(x, y+1))
            ret_list.append(f(x+1, y-1))
            ret_list.append(f(x+1, y))
        return ret_list

    def _apply_at_dist(self, node, apply_func, reduce_func, dist=1):
        if dist <= 0:
            return [apply_func(*node)]

        def from_neigbours(x, y):
            return self._apply_at_dist((x, y), apply_func, reduce_func, dist-1)
        values = self._apply(node, from_neigbours, default=set())
        values.append([apply_func(*node)])
        values = reduce_func(values)
        return values

    def upsize(self, x=0, y=0, incr=1, value=0):
        big_grid = type(self).from_order(self.order+incr)
        big_grid.set_all(value)

        small_mid = self.height // 2
        big_mid = big_grid.height // 2
        # diff_mid = big_mid - small_mid
        for _x, _y in self.index_generator():
            di = x+_x
            if di < 0 or di >= big_grid.height:
                continue
            x = 0
            if _x > small_mid:
                x += (_x-small_mid)
            if di > big_mid:
                x -= (di-big_mid)

            dj = y+_y+x
            if dj < 0 or dj >= len(big_grid.grid[di]):
                continue
            big_grid.grid[di][dj] = self.grid[_x][_y]

        return big_grid

    def _no_index_error(self, x, y):
        try:
            self.grid[x][y]
            if x < 0 or y < 0:
                return False
            else:
                return True
        except IndexError:
            return False

    def _get_hex(self, x, y, size=1):
        pass


class HexGridValidate(HexGridManipulate):

    def validate_hex(self, x, y):
        if not self._no_index_error(x, y):
            return True
        value = self[x, y]
        if value < 0:
            return False
        if value <= 1:
            return True
        wanted_digits = set(range(1, self[x, y]))

        def remove(_x, _y):
            wanted_digits.discard(self[_x, _y])
        self._apply((x, y), remove)
        if wanted_digits:
            return False
        return True


class HexGridVisualize(HexGridValidate):

    def print(self, indent=True, color=True, mark=None):
        print(self._print(indent=indent, color=color, mark=mark))
        return self

    def _print(self, indent=True, color=True, mark=set()):
        if indent:
            indent = " "
        else:
            indent = ""
        s = ""

        for x, row in enumerate(self.grid):
            if x < self.height/2:
                s += indent*(self.height-x)
            else:
                s += indent*(x+1)
            for y, value in enumerate(row):
                s += " "
                if color:
                    style = []

                    if mark is not None and (x, y) in mark:
                        style.append("3")
                        style.append("4")
                        style.append("5")
                        style.append("6")
                        style.append("51")
                    if value == 0:
                        style.append("1")
                        style.append("35")
                    elif not self.validate_hex(x,  y):
                        style.append("31")
                    # elif self.same_neighbour(x, y):
                    #     style.append("1")
                    #     style.append("38;2;255;135;0")
                    # elif self.check_perfect(x, y):
                    #     style.append("1")
                    #     style.append("32")
                    s += "\033[{}m".format(";".join(style))
                s += f"{value}"
                if color:
                    s += '\033[0;0;0m'
            s += "\n"
        return s


class HexGrid(HexGridVisualize):
    pass
