"""(보너스) N×N 십자가(Cross)와 X 패턴 자동 생성기."""

from src.matrix import make_matrix, set_value


def make_cross(n, on=1, off=0):
    """가운데 행과 가운데 열이 채워진 십자가 패턴."""
    m = make_matrix(n, off)
    mid = n // 2
    for k in range(n):
        set_value(m, mid, k, on)
        set_value(m, k, mid, on)
    return m


def make_x(n, on=1, off=0):
    """두 대각선이 채워진 X 패턴."""
    m = make_matrix(n, off)
    for k in range(n):
        set_value(m, k, k, on)
        set_value(m, k, n - 1 - k, on)
    return m
