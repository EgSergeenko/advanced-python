from typing import Generator


def fib_generator(n: int) -> Generator[int, None, None]:
    a, b = 1, 0
    for _ in range(n):
        yield b
        a, b = a + b, a
