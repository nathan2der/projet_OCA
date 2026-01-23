from __future__ import annotations

import time
from typing import Callable, Tuple, TypeVar

T = TypeVar("T")


def time_call(fn: Callable[[], T]) -> Tuple[T, float]:
    start = time.perf_counter()
    out = fn()
    end = time.perf_counter()
    return out, (end - start)
