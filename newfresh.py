from hexgrid import HexGrid
from functools import reduce
from itertools import chain, starmap


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

    def swapping(self):
        doublets = [
            self.swap_doublet_neighbour(*node)
            for node
            in self.index_generator()
            if self.neighbour_with_my_neigbour(*node)
        ]
        if doublets:
            return reduce(lambda a,b: a|b, doublets)
        else:
            return None

    def __call__(self):
        self.set_all(0)
        # self.print()
        mid = self.height // 2
        self.grid[mid][mid] = 7
        node_list = [(mid, mid)]
        while 0 in self.value_generator():
            new_list = []
            for node in node_list:
                new_list.extend(self._apply_on_neighbours(*node, self.give_value))
            node_list = [node for node in new_list if node is not None]
            # swapped = self.swapping()
            # self.print(mark=swapped)
            # print("-"*40)
        self.brute_upgrade()
        # self.print()
        return self

    def give_value(self, ix, jx):
        if self.grid[ix][jx] > 0:
            return None
        highest = self.highest_available(ix, jx)
        used_values = self.values_at_dist(ix, jx, dist=2)
        allowed_values = set(range(0, highest+1))
        needed = self.neigbour_needs(ix, jx)
        values = allowed_values - used_values
        values = (values & needed) or needed
        self.grid[ix][jx] = max(values or [highest])
        # self.print(mark={(ix, jx)})
        # print("-"*40)
        return ix, jx

    def do(self, ix, jx):
        if self.grid[ix][jx] > 0:
            return
        if 0 not in self.value_generator():
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
    .from_order(27)()
    .visualize(color=True)
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

grid = [
    (4, 3, 2),
    (2, 1, 3, 1),
    (3, 1, 5, 2, 4),
    (2, 1, 4, 3),
    (2, 3, 1)
]
# NewFreshAlg.from_grid(grid).visualize(color=False)
# print(NewFreshAlg.from_grid(grid).values_at_dist(2, 2, 2))