from hexgrid import HexGridVisualize
import time  # noqa:F401

# print(HexGridBase.from_order(1).grid)


grid = [
    (4, 3, 2),
    (2, 1, 3, 1),
    (3, 1, 5, 2, 4),
    (2, 1, 4, 3),
    (2, 3, 1)
]
grid = HexGridVisualize.from_grid(grid).print()
print(grid[1, 2], end="\n"+"-"*20+"\n")
print(grid[1, 2:4], end="\n"+"-"*20+"\n")
print(grid["list", 1, 2], end="\n"+"-"*20+"\n")
grid["grid", 1, 2].print()
grid["grid", 2, 2, 2].print()
# grid = [(2, 3), (4, 1, 4), (3, 2)]
# HexGrid.from_grid(grid).visualize()
# grid = [(4, 3, 4), (1, 2, 1, 2), (2, 3, 7, 4, 3), (4, 5, 6, 1), (1, 2, 3)]
# HexGrid.from_grid(grid).visualize()
# grid = [(3, 2, 1), (1, 6, 5, 4), (3, 4, 7, 3, 2), (2, 1, 2, 1), (0, 0, 0)]
# HexGrid.from_grid(grid).upsize(value=0).visualize()
# grid = [(3, 2, 1, 3), (1, 6, 5, 4, 2), (3, 4, 7, 3, 2, 1), (0, 2, 1, 2, 1, 0, 0), (0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0)]
# HexGrid.from_grid(grid).visualize()
# HexGrid.from_order(5).visualize()
# grid = [(4, 3, 4), (2, 1, 2, 1), (3, 4, 7, 3, 2), (1, 6, 5, 4), (3, 2, 1)]

# grid = [
#     (4, 3, 4, 0, 0),
#     (1, 2, 1, 2, 0, 0),
#     (2, 3, 7, 4, 3, 0, 0),
#     (0, 4, 5, 6, 1, 0, 0, 0),
#     (0, 0, 1, 2, 3, 0, 0, 0, 0),
#     (0, 4, 5, 6, 1, 0, 0, 0),
#     (2, 3, 7, 4, 3, 0, 0),
#     (1, 2, 1, 2, 0, 0),
#     (4, 3, 4, 0, 0),
# ]
# HexGrid.from_grid(grid).visualize()
# grid = [
#          [1, 4, 3, 4, 1],
#         [5, 2, 1, 2, 5, 2],
#       [4, 3, 4, 3, 4, 3, 1],
#      [1, 2, 1, 2, 1, 2, 5, 4],
#     [2, 3, 7, 4, 3, 7, 4, 3, 2],
#      [4, 5, 6, 1, 5, 6, 1, 1],
#       [1, 2, 3, 4, 2, 3, 4],
#         [3, 4, 1, 5, 1, 2],
#          [1, 3, 2, 3, 4],
# ]
# HexGrid.from_grid(grid).visualize()

# grid = [[3, 2, 1], [1, 5, 4, 3], [2, 3, 6, 5, 2], [1, 2, 7, 1], [4, 3, 4]]
# HexGrid.from_grid(grid).visualize()
# grid = [[3, 2, 1], [1, 6, 5, 4], [3, 4, 7, 3, 2], [2, 1, 2, 1], [4, 3, 4]]
# HexGrid.from_grid(grid).visualize()
