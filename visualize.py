from itertools import chain


def draw(hexes):
    height = len(hexes)
    for ix, hexe in enumerate(hexes):
        if ix < height/2:
            print(" "*(height-ix), end="")
        else:
            print(" "*(ix+1), end="")
        for hex in hexe:
            print(" %d" % hex, end="")
        print()


def create(n=3):
    width = n
    grid = list()
    while width <= 2*n-1:
        grid.append([0]*width)
        width += 1
    width -= 1
    while width > n:
        width -= 1
        grid.append([0]*width)
    return grid


def get_allowed(grid, ix, jx):
    order = len(grid[0])-1
    allowed = set()

    def add(i, j):
        try:
            if i >= 0 and j >= 0:
                allowed.add(grid[i][j])
        except IndexError:
            pass
    if ix < order:
        add(ix-1, jx-1)
        add(ix-1, jx)
        add(ix, jx-1)
        add(ix, jx+1)
        add(ix+1, jx)
        add(ix+1, jx+1)
    elif ix > order:
        add(ix-1, jx)
        add(ix-1, jx+1)
        add(ix, jx-1)
        add(ix, jx+1)
        add(ix+1, jx-1)
        add(ix+1, jx)
    else:
        add(ix-1, jx-1)
        add(ix-1, jx)
        add(ix, jx-1)
        add(ix, jx+1)
        add(ix+1, jx-1)
        add(ix+1, jx)
    highest = [x for kx, x in enumerate(sorted(allowed)) if kx+1 == x][-1] + 1
    return highest


def validate_hex(gird, ix, jx):
    order = len(grid[0])-1
    try:
        if ix < 0 or jx < 0:
            return True
        if grid[ix][jx] < 1:
            return False
    except IndexError:
        return True
    wanted_digits = set(range(1, grid[ix][jx]))

    def remove(i, j):
        try:
            if i >= 0 and j >= 0:
                wanted_digits.discard(grid[i][j])
        except IndexError:
            pass
    if ix < order:
        remove(ix-1, jx-1)
        remove(ix-1, jx)
        remove(ix, jx-1)
        remove(ix, jx+1)
        remove(ix+1, jx)
        remove(ix+1, jx+1)
    elif ix > order:
        remove(ix-1, jx)
        remove(ix-1, jx+1)
        remove(ix, jx-1)
        remove(ix, jx+1)
        remove(ix+1, jx-1)
        remove(ix+1, jx)
    else:
        remove(ix-1, jx-1)
        remove(ix-1, jx)
        remove(ix, jx-1)
        remove(ix, jx+1)
        remove(ix+1, jx-1)
        remove(ix+1, jx)
    if wanted_digits:
        return False
    return True


def validate_local(grid, ix, jx):
    order = len(grid[0])-1
    validate_hex(grid, ix, jx)
    if ix < order:
        validate_hex(grid, ix-1, jx-1)
        validate_hex(grid, ix-1, jx)
        validate_hex(grid, ix, jx-1)
        validate_hex(grid, ix, jx+1)
        validate_hex(grid, ix+1, jx)
        validate_hex(grid, ix+1, jx+1)
    elif ix > order:
        validate_hex(grid, ix-1, jx)
        validate_hex(grid, ix-1, jx+1)
        validate_hex(grid, ix, jx-1)
        validate_hex(grid, ix, jx+1)
        validate_hex(grid, ix+1, jx-1)
        validate_hex(grid, ix+1, jx)
    else:
        validate_hex(grid, ix-1, jx-1)
        validate_hex(grid, ix-1, jx)
        validate_hex(grid, ix, jx-1)
        validate_hex(grid, ix, jx+1)
        validate_hex(grid, ix+1, jx-1)
        validate_hex(grid, ix+1, jx)


def validate(grid):
    for ix, row in enumerate(grid):
        for jx, _ in enumerate(row):
            if not validate_hex(grid, ix, jx):
                return False
    return True


def score(grid):
    n = len(grid[0])-1
    deduct = 3 * n**2 + 3 * n + 1
    return sum(chain(*grid)) - deduct


def one_two(grid):
    i = 1
    for ix, row in enumerate(grid):
        for jx, _ in enumerate(row):
            grid[ix][jx] = i
            i = i % 2 + 1

    return grid


def one(grid):
    for ix, row in enumerate(grid):
        for jx, _ in enumerate(row):
            grid[ix][jx] = 1
    return grid


def brute_upgrade(grid):
    grid = one(grid)
    changed = True
    while changed:
        changed = False
        for ix, row in enumerate(grid):
            for jx, _ in enumerate(row):
                grid[ix][jx] += 1
                if not validate_local(grid, ix, jx):
                    # if not validate(grid):
                    grid[ix][jx] -= 1
                else:
                    changed = True

    return grid


def random():
    pass


def test(grid):
    draw(grid)
    print(validate(grid))
    print("score:", score(grid))


# grid = [
#     (4, 3, 2),
#     (2, 1, 3, 1),
#     (3, 1, 5, 2, 4),
#     (2, 1, 4, 3),
#     (2, 3, 1)
# ]
# test(grid)
grid = create(3)
test(brute_upgrade(grid))

grid = [
    [1, 2],
    [3, 1, 1],
    [1, 1]
]
# print(get_allowed(grid, 1, 1))
# test(grid)


# from PIL import Image, ImageDraw
# import hexgrid
# import morton

# image = Image.new("L", (1024,1024))
# draw = ImageDraw(image)

# center = hexgrid.Point(0, 0)


# draw.line()
# image.show()
