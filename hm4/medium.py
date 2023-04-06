import itertools
import math
import multiprocessing
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Callable

from tools import log_time


def init_worker():
    with open('artifacts/medium.txt', 'a') as log_file:
        log_file.write(
            'Initialized worker: time={0}\n'.format(
                datetime.now(),
            ),
        )


@log_time('artifacts/medium.txt')
def integrate(
    f: Callable[..., float],
    a: float,
    b: float,
    executor: type[ProcessPoolExecutor] | type[ThreadPoolExecutor],
    *,
    n_jobs: int = 1,
    n_iter: int = 1000,
) -> float:
    step = (b - a) / n_iter
    with executor(max_workers=n_jobs, initializer=init_worker) as pool:
        steps = pool.map(
            partial(integrate_step, f=f, a=a, step=step),
            range(n_iter),
        )
    return sum(steps)


def integrate_step(
    i: int, f: Callable[..., float], a: float, step: float,
) -> float:
    return f(a + i * step) * step


def main():
    executors = [ProcessPoolExecutor, ThreadPoolExecutor]
    n_jobs_range = list(range(1, multiprocessing.cpu_count() * 2 + 1))
    for executor, n_jobs in itertools.product(executors, n_jobs_range):
        integrate(
            math.cos,
            0,
            math.pi / 2,
            executor,
            n_jobs=n_jobs,
        )


if __name__ == '__main__':
    main()
