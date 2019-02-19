from hexgrid import HexGrid


class NewFreshAlg(HexGrid):

    def __call__(self):
        for ix, jx in self.index_generator():
            if ix == 0 or jx == 0 or ix == self.height-1 or jx == len(self.grid[ix]):
                self.grid[ix][jx] += 1
                if not self.validate_local(ix, jx):
                    self.grid[ix][jx] -= 1
        return self
