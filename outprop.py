from hexgrid import HexGrid


class OutPropagation(HexGrid):

    def __call__(self):
        mid = self.height // 2

        self.set(mid, mid, 1)

        def setto1_ifnotset(ix, jx):
            if not self.get(ix, jx):
                self.set(ix, jx, 1)

        while [val for val in self.value_generator() if val == 0]:
            l = [(ix, jx) for (ix, jx), val in self.generator() if val > 0]
            for ix, jx in l:
                self._apply_on_neighbours(ix, jx, setto1_ifnotset)
            self.upgrade_current()

        return self

    def upgrade_current(self):
        good = True
        while good:
            l = [((ix, jx), self.sum_neighbours(ix, jx)) for (ix, jx), val in self.generator() if val > 0]
            l = [item for item in l if item[1] > 0]
            good = False
            for node in sorted(l, key=lambda x: x[1]):
                self.grid[node[0][0]][node[0][1]] += 1
                if not self.validate_local(*node[0]):
                    self.grid[node[0][0]][node[0][1]] -= 1
                else:
                    good = True
                    # break - want to remove node, but we want new values for the others


# OutPropagation.from_order(5).set_all(0)().visualize()

# for n in range(3, 28):
#     grid = OutPropagation.from_order(n).set_all(0)()
#     # grid.visualize()
#     grid = Counter(chain(*grid.grid))

#     print(n, grid)
