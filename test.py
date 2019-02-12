from multiprocessing import Process, Manager, Lock
import random

manager = Manager()
glob = manager.Namespace()
glob.grid = [1, 2, 3, 4, 5, 6]
lock = Lock()
# grid = manager.list([[1, 2, 3], [4, 5, 6]])
# pool = Pool(4)


def f(glob, i):
    x = random.randint(0, 5)
    new_grid = glob.grid.copy()
    new_grid[x] = random.randint(0, 50)
    if sum(new_grid) > sum(glob.grid):
        lock.acquire()
        print(i, new_grid)
        lock.release()
        glob.grid = new_grid


if __name__ == "__main__":

    # {f(glob) for _ in range(15)}

    # {pool.apply(f, (glob,)) for _ in range(10)}
    ps = [Process(target=f, args=(glob, i)) for i in range(1000)]
    [p.start() for p in ps]
    [p.join() for p in ps]
    print(glob.grid)
