from multiprocessing import Process
from threading import Thread

from fib import fib
from tools import log_time

N = 10 ** 4
REPEAT = 10


def main() -> None:
    fib_sequential()
    fib_parallel(Process)
    fib_parallel(Thread)


@log_time('artifacts/easy.txt')
def fib_parallel(executor: type[Process] | type[Thread]) -> None:
    workers = []
    for _ in range(REPEAT):
        workers.append(
            executor(target=fib, args=(N, )),
        )
        workers[-1].start()
    for worker in workers:
        worker.join()


@log_time('artifacts/easy.txt')
def fib_sequential() -> None:
    for _ in range(REPEAT):
        fib(N)


if __name__ == '__main__':
    main()
