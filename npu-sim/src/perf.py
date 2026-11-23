"""MAC 연산 성능 측정. I/O를 제외하고 연산 함수 호출 구간만 잰다."""

import time

from src.generator import make_cross, make_x
from src.mac import mac, mac_flat
from src.matrix import flatten

REPEAT = 10  # 과제 최소 기준: 크기별 10회 반복 측정 후 평균


def time_call_ms(func, args, repeat=REPEAT):
    """func(*args)를 repeat번 호출해 1회 평균 시간(ms)을 반환한다."""
    func(*args)  # 워밍업 1회 (첫 호출의 캐시/할당 영향을 평균에서 제외)
    elapsed = 0.0
    for _ in range(repeat):
        t0 = time.perf_counter()
        func(*args)
        elapsed += time.perf_counter() - t0
    return elapsed / repeat * 1000


def measure_sizes(sizes, filters=None, repeat=REPEAT):
    """크기별 평균 MAC 시간(2D, 1D)을 측정한다.

    filters에 해당 크기의 실제 Cross 필터가 있으면 그것을 쓰고,
    없으면 생성기로 만든 필터를 쓴다. 입력 패턴은 생성기의 X 패턴.
    """
    rows = []
    for n in sizes:
        filt = None
        if filters and n in filters:
            filt = filters[n].get("Cross")
        if filt is None:
            filt = make_cross(n)
        pattern = make_x(n)

        ms_2d = time_call_ms(mac, (pattern, filt), repeat)
        p_flat, f_flat = flatten(pattern), flatten(filt)  # 변환 시간은 측정에서 제외
        ms_1d = time_call_ms(mac_flat, (p_flat, f_flat), repeat)
        rows.append((n, ms_2d, ms_1d, n * n))
    return rows


def print_perf_table(rows, repeat=REPEAT):
    print(f"{'크기(N×N)':<10}{'평균 시간(ms)':>14}{'연산 횟수(N²)':>14}{'N²당 시간(ns)':>15}")
    print("-" * 56)
    for n, ms_2d, _, ops in rows:
        per_op_ns = ms_2d * 1e6 / ops
        print(f"{f'{n}×{n}':<10}{ms_2d:>14.4f}{ops:>14}{per_op_ns:>15.1f}")
    print(f"(측정: 크기별 {repeat}회 반복 평균, 워밍업 1회 제외, 연산 함수 호출 구간만)")


def print_flat_compare(rows, repeat=REPEAT):
    print(f"{'크기(N×N)':<10}{'2D 평균(ms)':>13}{'1D 평균(ms)':>13}{'1D/2D':>9}")
    print("-" * 45)
    for n, ms_2d, ms_1d, _ in rows:
        ratio = ms_1d / ms_2d if ms_2d > 0 else float("nan")
        print(f"{f'{n}×{n}':<10}{ms_2d:>13.4f}{ms_1d:>13.4f}{ratio:>9.2f}")
    print(f"(동일 입력, 동일 반복 횟수 {repeat}회)")
