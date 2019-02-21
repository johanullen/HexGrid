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
        # self.grid[-1][-1] = 1

        def setto1_ifnotset(ix, jx):
            if not self.get(ix, jx):
                self.set(ix, jx, 1)
        cnt = 0
        while [val for val in self.value_generator() if val == 0]:
            cnt += 1
            node_list = [(ix, jx) for (ix, jx), val in self.generator() if val > 0]
            for ix, jx in node_list:
                self._apply_on_neighbours(ix, jx, setto1_ifnotset)
            self.upgrade_current()
            # print(self._print())
        print("iterations: %d" % cnt)
        return self

    def _sorted(self, node):
        def eval_node(i, j):
            value = self.grid[i][j]
            neighbour_sum = self.sum_neighbours(i, j)
            same_neighbour = int(bool(self.same_neighbour(i, j)))
            neighbour_with_my_neigbour = int(bool(self.neighbour_with_my_neigbour(i, j)))
            prio = bool(neighbour_with_my_neigbour) and value == 1
            # return value + neighbour_sum + same_neighbour * 1 + neighbour_with_my_neigbour * 100
            return \
                neighbour_with_my_neigbour * 100 + \
                same_neighbour * 100 + \
                neighbour_sum + \
                value * 2 + \
                prio*50 * (7 - value)

        node_list = [
            ((ix, jx), eval_node(ix, jx))
            for (ix, jx), val
            in self.generator()
            if val > 0 and (ix, jx) != node
        ]
        # node_list = [item for item in node_list if item[1] > 0]

        return sorted(node_list, key=lambda x: x[1], reverse=True)

    def upgrade_current(self):
        good = True
        node = None
        cnt = 0
        while good:
            print(self._print())
            good = False
            node_list = self._sorted(node)
            # if cnt % len(node_list)*10 == 0:
            #     self.lower_all(1)
            #     print(self._print())
            freq = (len(node_list) // 4) or 1
            for (ix, jx), _ in node_list:
                self.grid[ix][jx] += 1
                if not self.validate_local(ix, jx):
                    self.grid[ix][jx] -= 1
                    node = (ix, jx)
                else:
                    good = True
                    cnt += 1
                    if cnt % freq == 0:
                        break


OutPropagation.from_order(27).set_all(0)().visualize()

# for n in range(3, 28):
#     grid = OutPropagation.from_order(n).set_all(0)()
#     # grid.visualize()
#     grid = Counter(chain(*grid.grid))

#     print(n, grid)
