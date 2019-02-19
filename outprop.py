from hexgrid import HexGrid


class OutPropagation(HexGrid):

    def __call__(self):
        mid = self.height // 2

        # self.set(mid, mid, 1)
        self.grid[0][0] = 1
        # self.grid[0][-1] = 1
        # self.grid[mid][0] = 1
        # self.grid[mid][-1] = 1
        # self.grid[-1][0] = 1
        self.grid[-1][-1] = 1

        def setto1_ifnotset(ix, jx):
            if not self.get(ix, jx):
                self.set(ix, jx, 1)

        while [val for val in self.value_generator() if val == 0]:
            l = [(ix, jx) for (ix, jx), val in self.generator() if val > 0]
            for ix, jx in l:
                self._apply_on_neighbours(ix, jx, setto1_ifnotset)
            self.upgrade_current()
            # print(self._print())

        return self

    def upgrade_current(self):
        good = True
        reverse = True
        remove_node = False
        node = None
        node_list = []
        cnt = 0
        while good:
            # print(self._print())
            if remove_node:
                node_list = [n for n in node_list if n is not node]
                remove_node = False
            else:
                node_list = [((ix, jx), self.sum_neighbours(ix, jx)) for (ix, jx), val in self.generator() if val > 0]
                node_list = [item for item in node_list if item[1] > 0]
                good = False
                freq = (len(node_list) // 4) or 1
            # reverse = not reverse
            # chose a node that has the same value as neighbour
            for node in sorted(node_list, key=lambda x: x[1], reverse=reverse):
                self.grid[node[0][0]][node[0][1]] += 1
                if not self.validate_local(*node[0]):
                    self.grid[node[0][0]][node[0][1]] -= 1
                else:
                    good = True
                    # break - want to remove node, but we want new values for the others
                    cnt += 1
                    if cnt % freq == 0:
                        remove_node = True
                        break


OutPropagation.from_order(27).set_all(0)().visualize()

# for n in range(3, 28):
#     grid = OutPropagation.from_order(n).set_all(0)()
#     # grid.visualize()
#     grid = Counter(chain(*grid.grid))

#     print(n, grid)
