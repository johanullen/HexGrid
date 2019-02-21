import random
from multiprocessing import Process, Manager, Lock
from itertools import chain as chain
from collections import Counter
from functools import reduce


class HexGrid:

    def __init__(self, grid, order, height, size):
        self.order = order
        self.grid = grid
        self.height = height
        self.size = size
        self.indices = list(self.index_generator())

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

    def upsize(self, ix=0, jx=0, incr=1, value=0):
        big_grid = type(self).from_order(self.order+incr)
        big_grid.set_all(value)

        small_mid = self.height // 2
        big_mid = big_grid.height // 2
        # diff_mid = big_mid - small_mid
        for i, j in self.index_generator():
            di = ix+i
            if di < 0 or di >= big_grid.height:
                continue
            x = 0
            if i > small_mid:
                x += (i-small_mid)
            if di > big_mid:
                x -= (di-big_mid)

            dj = jx+j+x
            if dj < 0 or dj >= len(big_grid.grid[di]):
                continue
            big_grid.grid[di][dj] = self.grid[i][j]

        return big_grid

    def _no_index_error(self, ix, jx):
        try:
            self.grid[ix][jx]
            if ix < 0 or jx < 0:
                return False
            else:
                return True
        except IndexError:
            return False

    def _apply_on_neighbours(self, ix, jx, ff, default=None):
        def f(i, j):
            if self._no_index_error(i, j):
                return ff(i, j)
            else:
                return default

        r = list()
        if ix < self.order-1:
            r.append(f(ix-1, jx-1))
            r.append(f(ix-1, jx))
            r.append(f(ix, jx-1))
            r.append(f(ix, jx+1))
            r.append(f(ix+1, jx))
            r.append(f(ix+1, jx+1))
        elif ix > self.order-1:
            r.append(f(ix-1, jx))
            r.append(f(ix-1, jx+1))
            r.append(f(ix, jx-1))
            r.append(f(ix, jx+1))
            r.append(f(ix+1, jx-1))
            r.append(f(ix+1, jx))
        else:
            r.append(f(ix-1, jx-1))
            r.append(f(ix-1, jx))
            r.append(f(ix, jx-1))
            r.append(f(ix, jx+1))
            r.append(f(ix+1, jx-1))
            r.append(f(ix+1, jx))
        return r

    def check_perfect(self, ix, jx):
        # values = set(range(1, self.highest_possible(ix, jx)+1))
        # value = self.get(ix, jx)
        # values.discard(value)
        values = {self.get(ix, jx)}

        def remove(i, j):
            if self.grid[i][j] in values:
                return False
            values.add(self.grid[i][j])
            return True
            # values.discard(self.grid[i][j])
        dups = self._apply_on_neighbours(ix, jx, remove)
        return False not in dups

    def validate_hex(self, ix, jx):
        if not self._no_index_error(ix, jx):
            return True
        value = self.grid[ix][jx]
        if value < 0:
            return False
        if value <= 1:
            return True
        wanted_digits = set(range(1, self.grid[ix][jx]))

        def remove(i, j):
            wanted_digits.discard(self.grid[i][j])
        self._apply_on_neighbours(ix, jx, remove)
        if wanted_digits:
            return False
        return True

    def validate_local(self, ix, jx):
        valid = [self.validate_hex(ix, jx)]
        valid += self._apply_on_neighbours(ix, jx, self.validate_hex, True)
        return False not in valid

    def validate(self):
        for ix, row in enumerate(self.grid):
            for jx, _ in enumerate(row):
                if not self.validate_hex(ix, jx):
                    return False
        return True

    def get_allowed(self, ix, jx):
        available = set()

        def add(i, j):
            available.add(self.grid[i][j])

        self._apply_on_neighbours(ix, jx, add)
        allowed = [x for kx, x in enumerate(sorted(available)) if kx+1 == x]
        if allowed:
            highest = min(allowed[-1] + 1, self.highest_possible(ix, jx))
        else:
            highest = 1
        return highest

    def has_nonempty_neighbour(self, ix, jx):
        def has_value(i, j):
            return self.get_or_zero(i, j) > 0
        return True in self._apply_on_neighbours(ix, jx, has_value)

    def values_at_dist(self, ix, jx, dist=1):
        if dist <= 0:
            return {self.get(ix, jx)}

        def from_neigbours(i, j):
            return self.values_at_dist(i, j, dist-1)
        values = self._apply_on_neighbours(ix, jx, from_neigbours, set())
        values = reduce(lambda a, b: a | b, values)
        values.add(self.get(ix, jx))
        return values

    def same_neighbour(self, ix, jx):
        value = self.get(ix, jx)
        if not value:
            return 0

        def check_neigbour(i, j):
            return self.get(i, j) == value
        return sum(self._apply_on_neighbours(ix, jx, check_neigbour, 0))

    def neighbour_with_my_neigbour(self, ix, jx):
        value = self.get(ix, jx)
        if not value:
            return 0

        def check_neigbour_neigbours(i, j):
            def check_neigbour(ii, jj):
                return self.get(i, j) == value
            return sum(self._apply_on_neighbours(ix, jx, check_neigbour, 0))
        return sum(self._apply_on_neighbours(ix, jx, check_neigbour_neigbours, 0))

    def highest_possible(self, ix, jx):
        if ix == 0 or ix == self.height-1:
            if jx == 0 or jx == len(self.grid[ix])-1:
                return 4
            else:
                return 5
        elif ix == self.height//2:
            if jx == 0 or jx == len(self.grid[ix])-1:
                return 4
            else:
                return 7
        else:
            if jx == 0 or jx == len(self.grid[ix])-1:
                return 5
            else:
                return 7

    def highest_available(self, ix, jx):
        existing_values = self.available_values_from_neigbours(ix, jx)
        existing_values = [values for values in existing_values if values]
        existing_values = sorted(reduce(lambda a,b: a|b, existing_values))[:len(existing_values)]
        highest_neighbours = max([value for index, value in enumerate(existing_values) if index+1==value] or [1])
        highest_self = self.highest_possible(ix, jx)
        highest = min((highest_self, highest_neighbours))
        return highest

    def empty_neigbours(self, ix, jx):
        def is_empty(i, j):
            return not self.grid[i][j]
        return sum(self._apply_on_neighbours(ix, jx, is_empty))

    def available_values_from_neigbours(self, ix, jx):
        def available_values(i, j):
            if self.grid[i][j] > 0:
                return {self.grid[i][j]}
            else:
                return set(range(1, self.highest_possible(i, j)+1))
        return self._apply_on_neighbours(ix, jx, available_values, set())

    def neigbour_needs(self, ix, jx):
        def needs(i, j):
            available = self.values_at_dist(i, j, dist=1)
            needed = set(range(1, self.grid[i][j]))
            return needed - available
        needed = self._apply_on_neighbours(ix, jx, needs, set())
        needed = reduce(lambda a,b: a|b, needed)
        return needed

    def get(self, ix, jx):
        if ix < 0:
            raise IndexError("ix < 0")
        elif jx < 0:
            raise IndexError("jx < 0")
        else:
            return self.grid[ix][jx]

    def get_or_zero(self, ix, jx):
        try:
            return self.get(ix, jx)
        except IndexError:
            return 0

    def set_value(self, ix, jx, val):
        if ix < 0:
            raise IndexError("ix < 0")
        elif jx < 0:
            raise IndexError("jx < 0")
        else:
            self.grid[ix][jx] = val
        return self

    def set_or_ignore(self, ix, jx, val):
        try:
            self.set_value(ix, jx, val)
        except IndexError:
            pass

    def set_all(self, val):
        for ix, jx in self.index_generator():
            self.set_value(ix, jx, val)
        return self

    def lower_all(self, value=1):
        for ix, jx in self.index_generator():
            if self.grid[ix][jx] >= 1:
                self.grid[ix][jx] = max(self.grid[ix][jx]-value, 1)
        return self

    def lower_invalid(self):
        while not self.validate():
            for ix, jx in self.index_generator():
                while not self.validate_hex(ix, jx):
                    self.grid[ix][jx] -=1
        return self

    def swap_doublet_neighbour(self, ix, jx):
        if self.grid[ix][jx] <= 0:
            return
        if not self.same_neighbour(ix, jx):
            return
        # print("want to swap", ix, jx)
        swapped = []
        def swap(i, j):
            if self.grid[i][j] <= 0:
                return
            if swapped:
                return
            if self.grid[ix][jx] == self.grid[i][j]:
                return
            if not self.same_neighbour(i, j):
                return
            # print("swapping", ix, jx, i, j)
            tmp = self.grid[ix][jx]
            self.grid[ix][jx] = self.grid[i][j]
            self.grid[i][j] = tmp
            # this is probably not needed
            # if not self.validate_hex(ix, jx) or not self.validate_hex(i, j):
            #     tmp = self.grid[ix][jx]
            #     self.grid[ix][jx] = self.grid[i][j]
            #     self.grid[i][j] = tmp
            #     return

            swapped.append((i, j))
        self._apply_on_neighbours(ix, jx, swap)
        if swapped:
            return {(ix, jx), swapped[0]}
        else:
            return set()


    def score(self):
        return sum([hex for row in self.grid for hex in row]) - self.size

    def sum_perfect(self):
        return sum([1 for ix, jx in self.index_generator() if self.check_perfect(ix, jx)])

    def sum_same_neighbour(self):
        return sum([1 for ix, jx in self.index_generator() if self.same_neighbour(ix, jx)])

    def sum_invalid(self):
        return sum([1 for ix, jx in self.index_generator() if not self.validate_hex(ix, jx)])

    def sum_neighbours(self, ix, jx):
        return sum(self._apply_on_neighbours(ix, jx, self.get, 0))

    def index_generator(self):
        for ix, row in enumerate(self.grid):
            for jx, _ in enumerate(row):
                yield(ix, jx)

    def value_generator(self):
        for row in self.grid:
            for val in row:
                yield(val)

    def generator(self):
        for ix, row in enumerate(self.grid):
            for jx, val in enumerate(row):
                yield((ix, jx), val)

    def print(self, indent=True, color=True, mark=None):
        print(self._print(indent=indent, color=color, mark=mark))
        return self

    def _print(self, indent=True, color=True, mark=set()):
        if indent:
            indent = " "
        else:
            indent = ""
        s = ""

        for ix, row in enumerate(self.grid):
            if ix < self.height/2:
                s += indent*(self.height-ix)
            else:
                s += indent*(ix+1)
            for jx, value in enumerate(row):
                s += " "
                if color:
                    style = []

                    if mark is not None and (ix, jx) in mark:
                        style.append("3")
                        style.append("4")
                        style.append("5")
                        style.append("6")
                        style.append("51")
                    if value == 0:
                        style.append("1")
                        style.append("35")
                    elif not self.validate_hex(ix,  jx):
                        style.append("31")
                    elif self.same_neighbour(ix, jx):
                        style.append("1")
                        style.append("38;2;255;135;0")
                    elif self.check_perfect(ix, jx):
                        style.append("1")
                        style.append("32")
                    s += "\033[%sm" % ";".join(style)
                s += "%d" % value
                if color:
                    s += '\033[0;0;0m'
            s += "\n"
        return s

    def __str__(self):
        return self._print()

    def __repr__(self):
        return self.__str__()

    def prt(self):
        return "(" + str(self.grid).replace("[", "(").replace("]", ")")[1:-1] + ")"

    def dist(self):
        return Counter(chain(*self.grid))

    def visualize(self, indent=True, color=True, mark=None):
        print("*"*40)
        print("CLASS:", type(self))
        print(self._print(indent=indent, color=color, mark=mark))
        print("n:    ", self.order)
        print("size: ", self.size)
        print("VALID:", self.validate())
        print("SCORE:", self.score())
        print("-"*40)
        print("DIST: ")
        dist = self.dist()
        max_dist = max(dist.values())
        for val, count in dist.items():
            print("\t%d: %5d %s" % (val, count, "*"*int(count*40/max_dist)))
        print("PERFECT:", self.sum_perfect())
        print("SAME NEIGHBOUR:", self.sum_same_neighbour())
        print("INVALID:", self.sum_invalid())
        print("-"*40)
        print("GRID: ", self.prt())
        print("*"*40)
        return self

    def brute_upgrade(self):
        changed = True
        while changed:
            changed = False
            for ix, jx in self.index_generator():
                self.grid[ix][jx] += 1
                if not self.validate_local(ix, jx):
                    self.grid[ix][jx] -= 1
                else:
                    changed = True
        return self

    def _get_random_index(self):
        return random.choice(self.indices)

    def _random_change(self, upgrades=None):
        if upgrades is None:
            upgrades = self.size//2
        for _ in range(upgrades):
            ix, jx = self._get_random_index()
            highest = self.get_allowed(ix, jx)
            old_val = self.get(ix, jx)
            self.set_value(ix, jx, random.randint(1, highest))
            if not self.validate_local(ix, jx):
                self.set_value(ix, jx, old_val)
        return self

    def _random_upgrade(self, upgrades=None):
        if upgrades is None:
            upgrades = self.size
        for _ in range(upgrades):
            ix, jx = self._get_random_index()
            old_val = self.get(ix, jx)
            self.set_value(ix, jx, old_val+1)
            if not self.validate_local(ix, jx):
                self.set_value(ix, jx, old_val)
            self.brute_upgrade()
        return self

    def _random(self, random_changes=None, random_upgrades=None, tries=100):
        manager = Manager()
        glob = manager.Namespace()
        # start = time.time()
        glob.best_grid = self.copy()
        glob.best_score = glob.best_grid.score()
        lock = Lock()

        def f(i, glob, lock):
            start_grid = self.copy()
            start_grid._random_upgrade(random_upgrades)
            # start_grid._random_change(random_changes)
            # start_grid.brute_upgrade()
            score = start_grid.score()
            with lock:
                if score > glob.best_score:
                    print(i, score)
                    glob.best_grid = start_grid.copy()
                    glob.best_score = score
            return
        ps = [Process(target=f, args=(i, glob, lock)) for i in range(tries)]
        [p.start() for p in ps]
        [p.join() for p in ps]

        # try:

        # except KeyboardInterrupt:
        #     pass
        self = glob.best_grid
        # print("%d : %d : %.2fs" % (i, score, (time.time()-start)))
        return self

    def downgrade7(self, to=1):
        for (ix, jx), val in self.generator():
            if val == 7:
                self.set_value(ix, jx, to)
        return self

    def __call__(self):
        self.set_all(1)
        return self.brute_upgrade()
