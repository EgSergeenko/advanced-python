import copy
import numbers
import os
from typing import Any, Iterable

import numpy as np


class HashMixin(object):
    def __hash__(self) -> int:
        # The remainder of dividing the sum of the matrix elements
        # by a prime number
        return sum([sum(row) for row in self.value]) % 47


class RepresentationMixin(object):
    def __str__(self) -> str:
        row_strings = [
            self.row_to_string(row) for row in self.value
        ]
        return '\n'.join(row_strings)

    def __repr__(self) -> str:
        return str(self)

    def row_to_string(self, row: Iterable[Any]) -> str:
        return ' '.join(
            [str(value).rjust(5) for value in row],
        )


class IOMixin(object):
    def to_txt(self, output_path: str) -> None:
        with open(output_path, 'w') as output_file:
            output_file.write(str(self))


class ValueMixin(object):
    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = self._preprocess(value)

    def _preprocess(self, value: Any) -> Any:
        return value


class Matrix(HashMixin, RepresentationMixin, IOMixin, ValueMixin):
    def __init__(self, value: list[list[float]]) -> None:
        self.value = value
        self._cache: dict[tuple[int, int], Matrix] = {}

    def __add__(self, other: 'Matrix') -> 'Matrix':
        self._check_shapes(other, 'add')

        output = self._get_output_matrix(self.shape)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                output[i][j] = self.value[i][j] + other.value[i][j]

        return Matrix(output)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        self._check_shapes(other, 'mul')

        output = self._get_output_matrix(self.shape)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                output[i][j] = self.value[i][j] * other.value[i][j]

        return Matrix(output)

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        self._check_shapes(other, 'matmul')

        cache_key = (hash(self), hash(other))
        cached_output = self._cache.get(cache_key)
        if cached_output is not None:
            return cached_output

        output = self._get_output_matrix((self.shape[0], other.shape[1]))

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                pairs = zip(self.get_row(i), other.get_column(j))
                output[i][j] = sum((p[0] * p[1] for p in pairs))

        self._cache[cache_key] = Matrix(output)

        return Matrix(output)

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.value), len(self.value[0])

    def get_row(self, idx: int) -> list[float]:
        return self.value[idx]

    def get_column(self, idx: int) -> list[float]:
        return [row[idx] for row in self.value]

    def _get_output_matrix(self, shape: tuple[int, int]) -> list[list[float]]:
        output = []
        for _ in range(shape[0]):
            output.append([float(0)] * shape[1])
        return output

    def _check_shapes(self, other: 'Matrix', operation: str) -> None:
        if operation == 'matmul':
            check_result = self.shape[1] == other.shape[0]
        else:
            check_result = self.shape == other.shape

        if not check_result:
            raise ValueError(
                'operands could not be broadcast together with shapes {0} {1}'.format(
                    self.shape, other.shape,
                ),
            )

    def _preprocess(self, value: list[list[float]]) -> list[list[float]]:
        return copy.deepcopy(value)


class ArrayLike(
    np.lib.mixins.NDArrayOperatorsMixin,
    RepresentationMixin,
    IOMixin,
    ValueMixin,
):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __init__(self, value: int | float | Iterable | np.ndarray) -> None:
        self.value = value

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):
                return NotImplemented
        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def _preprocess(
        self, value: int | float | Iterable | np.ndarray,
    ) -> np.ndarray:
        return np.asarray(value)


def generate_data(shape: tuple[int, int]) -> list[list[float]]:
    return np.random.randint(0, 10, (shape)).tolist()


def matrix_equality(matrix1: Matrix, matrix2: Matrix) -> bool:
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if matrix1.value[i][j] != matrix2.value[i][j]:
                return False
    return True


def check_collision(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> bool:
    conditions = [
        hash(a) == hash(c),
        not matrix_equality(a, c),
        matrix_equality(b, d),
        not matrix_equality(a @ b, c @ d),
    ]

    return all(conditions)


def easy() -> None:
    output_dir = os.path.join('artifacts', 'easy')

    m1 = Matrix(generate_data((10, 10)))
    m2 = Matrix(generate_data((10, 10)))

    filenames = [
        'matrix+.txt', 'matrix*.txt', 'matrix@.txt',
    ]
    matrices = [m1 + m2, m1 * m2, m1 @ m2]
    filepaths = [
        os.path.join(output_dir, filename) for filename in filenames
    ]
    for matrix, output_path in zip(matrices, filepaths):
        matrix.to_txt(output_path)


def medium() -> None:
    output_dir = os.path.join('artifacts', 'medium')

    m1 = ArrayLike(generate_data((10, 10)))
    m2 = ArrayLike(generate_data((10, 10)))

    filenames = [
        'matrix+.txt', 'matrix*.txt', 'matrix@.txt',
    ]
    matrices = [m1 + m2, m1 * m2, m1 @ m2]
    filepaths = [
        os.path.join(output_dir, filename) for filename in filenames
    ]
    for matrix, output_path in zip(matrices, filepaths):
        matrix.to_txt(output_path)


def hard() -> None:
    output_dir = os.path.join('artifacts', 'hard')

    while True:
        a = Matrix(generate_data((2, 2)))
        b = Matrix(generate_data((2, 2)))
        c = Matrix(generate_data((2, 2)))
        d = Matrix(b.value)

        if check_collision(a, b, c, d):
            ab, cd = a @ b, c @ d

            filenames = [
                'A.txt', 'B.txt', 'C.txt', 'D.txt', 'AB.txt', 'CD.txt',
            ]
            filepaths = [
                os.path.join(output_dir, filename) for filename in filenames
            ]
            matrices = [a, b, c, d, ab, cd]
            for matrix, output_path in zip(matrices, filepaths):
                matrix.to_txt(output_path)

            with open(os.path.join(output_dir, 'hash.txt'), 'w') as hash_file:
                hash_file.write('Hash AB: {0}\n'.format(hash(ab)))
                hash_file.write('Hash CD: {0}\n'.format(hash(cd)))

            return


if __name__ == '__main__':
    np.random.seed(0)
    easy()
    medium()
    hard()
