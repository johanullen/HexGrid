from hexgrid import HexGrid


class BuildPerfectly(HexGrid):
    def __call__(self):
        return self


BuildPerfectly.from_order(2)().visualize()