from hexgrid import HexGrid


class RandomChange(HexGrid):
    def __init__(self, *args, **kwargs):
        (HexGrid).__init__(self, *args, **kwargs)
        self.indices = list(self.index_generator())

    def __call__(self, *, start_value=1, random_changes=None, random_upgrades=None, tries=5):
        self.set_all(start_value)
        # self.set_all(1).set(2, 2, 7)
        return self._random(random_changes, random_upgrades, tries)


RandomChange.from_order(5)(tries=100).visualize()
