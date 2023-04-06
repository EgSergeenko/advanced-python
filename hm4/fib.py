def fib(n: int) -> list[int]:
    if n == 0:
        return []
    if n == 1:
        return [0]
    a, b = 1, 0
    sequence = [b, a]
    for _ in range(2, n):
        a, b = a + b, a
        sequence.append(a)
    return sequence
