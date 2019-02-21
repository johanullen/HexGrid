from hexgrid import HexGrid
from functools import reduce
from itertools import chain


class NewFreshAlg(HexGrid):

    def neigbours(self, ix, jx):
        highest_possible = self.highest_possible(ix, jx)
        values = set(range(1, highest_possible+1))
        values.discard(self.grid[ix][jx])
        missing_values = set(range(1, self.grid[ix][jx]))
        free_nodes = list()

        def discard_values(i, j):
            values.discard(self.grid[i][j])
            missing_values.discard(self.grid[i][j])
            free_nodes.append((i, j))
        self._apply_on_neighbours(ix, jx, discard_values)
        if not values:
            values = set(range(1, highest_possible+1))
        print(ix, jx, values, missing_values)
        return frozenset(values), frozenset(missing_values)

    def __call__(self):
        self.set_all(0)
        print(self._print())
        mid = self.height // 2
        self.grid[mid][mid] = 7
        node_list = [(mid, mid)]
        while 0 in chain(*self.grid):
            new_list = []
            for node in node_list:
                new_list.extend(self._apply_on_neighbours(*node, self.do))
            node_list = [node for node in new_list if node is not None]
        return self

    def do(self, ix, jx):
        if self.grid[ix][jx] > 0:
            return
        if 0 not in chain(*self.grid):
            return
        print(ix, jx)
        print("---")
        values, missing_values = zip(*self._apply_on_neighbours(
            ix, jx,
            self.neigbours,
            (frozenset(range(1, 8)), frozenset({}))
        ))
        print(values)
        print(missing_values)

        def intersect(a, b):
            return a & b
        def union(a, b):
            return a | b
        values = reduce(intersect, values)
        missing_values = reduce(union, missing_values)
        print("a", values, missing_values)
        allowed = set(range(1, self.highest_possible(ix, jx)+1))
        values &= allowed
        print("b", values, missing_values)
        if not values & missing_values and missing_values:
            values = missing_values
        print("c", values)
        if not values:
            values = allowed
        print("d", values)

        self.set(ix, jx, max(values))
        print(self._print())
        print("-"*40)

        return ix, jx
        # while not self.validate_hex(ix, jx):
        #     self.grid[ix][jx] -= 1


(
    NewFreshAlg
    .from_order(4)()
    .visualize()
    # .lower_all()
    # .print()
    # .lower_invalid()
    # .print()
    # ._random_upgrade(1000)
    # .print()
    # .brute_upgrade()
    # .print()
    # .visualize()
)
