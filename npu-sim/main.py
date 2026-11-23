"""Mini NPU Simulator - 실행 진입점.

사용법:
    python main.py                 # 모드 선택 메뉴
    python main.py 다른파일.json   # 모드 2에서 읽을 JSON 경로 지정 (기본: main.py 옆 data.json)
"""

import os
import sys

from src.console import ask, fmt_score, section
from src.generator import make_cross, make_x
from src.judge import judge
from src.mac import mac
from src.mode_input import run_mode_1
from src.mode_json import run_mode_2
from src.perf import REPEAT, measure_sizes, print_flat_compare, print_perf_table

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(BASE_DIR, "data.json")


def run_mode_3():
    """(보너스) 패턴 생성기: N을 입력받아 N×N Cross/X를 만들고 판정·성능 분석에 재사용한다."""
    while True:
        text = ask("생성할 크기 N (3 이상 정수): ").strip()
        if text.isdigit() and int(text) >= 3:
            n = int(text)
            break
        print("입력 형식 오류: 3 이상의 정수를 입력하세요.")

    cross_f, x_f = make_cross(n), make_x(n)
    section(f"[1] 생성된 {n}×{n} 패턴으로 판정")
    for name, pattern in (("Cross 패턴", cross_f), ("X 패턴", x_f)):
        sc, sx = mac(pattern, cross_f), mac(pattern, x_f)
        print(f"{name}: Cross 점수 {fmt_score(sc)} / X 점수 {fmt_score(sx)} → 판정 {judge(sc, sx)}")

    section(f"[2] 성능 분석 (평균/{REPEAT}회)")
    rows = measure_sizes([n], {n: {"Cross": cross_f}})
    print_perf_table(rows)
    print()
    print_flat_compare(rows)


def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA

    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. 패턴 생성기 (보너스)")
    while True:
        choice = ask("선택: ").strip()
        if choice in ("1", "2", "3"):
            break
        print("1, 2, 3 중 하나를 입력하세요.")

    if choice == "1":
        run_mode_1()
    elif choice == "2":
        run_mode_2(data_path)
    else:
        run_mode_3()


if __name__ == "__main__":
    main()
