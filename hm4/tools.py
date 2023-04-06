import time
from functools import wraps
from typing import Any, Callable, TypeVar, cast

FuncT = TypeVar('FuncT', bound=Callable[..., Any])


def log_time(log_path: str) -> FuncT:
    def log_time_decorator(func: FuncT) -> FuncT:
        @wraps(func)
        def log_time_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            with open(log_path, 'a') as log_file:
                log_file.write(
                    'Func execution info: name={0}, args={1}, kwargs={2}, Δtime={3:.5f}\n'.format(
                        func.__name__, args, kwargs, end - start,
                    ),
                )
            return result
        return cast(FuncT, log_time_wrapper)
    return cast(FuncT, log_time_decorator)
