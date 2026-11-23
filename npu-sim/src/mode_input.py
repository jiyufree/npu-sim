"""모드 1: 콘솔에서 3×3 필터 A, B와 패턴을 입력받아 판정한다."""

from src.console import ask, fmt_score, section
from src.judge import EPSILON, UNDECIDED, judge
from src.mac import mac
from src.matrix import format_matrix
from src.perf import REPEAT, measure_sizes, print_perf_table, time_call_ms


def parse_number(text):
    """정수면 int, 소수면 float로 변환한다. 숫자가 아니면 ValueError."""
    try:
        return int(text)
    except ValueError:
        return float(text)  # 여기서도 실패하면 ValueError가 호출자로 전달된다


def read_matrix(name, n=3):
    """n줄을 한 줄씩(공백 구분) 입력받는다. 형식 오류면 처음부터 다시 입력받는다."""
    print(f"{name} ({n}줄 입력, 공백 구분)")
    while True:
        rows = []
        for i in range(n):
            parts = ask(f"  {i + 1}행: ").split()

            if len(parts) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요. "
                      f"({i + 1}행에 {len(parts)}개 입력됨)")
                break
            try:
                rows.append([parse_number(p) for p in parts])
            except ValueError:
                print("입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다. 숫자만 입력하세요.")
                break

        if len(rows) == n:
            return rows
        print(f"→ {name}를 처음부터 다시 입력하세요.")


def run_mode_1():
    section("[1] 필터 입력")
    filter_a = read_matrix("필터 A")
    print("✓ 필터 A 저장 완료:")
    print(format_matrix(filter_a))
    print()
    filter_b = read_matrix("필터 B")
    print("✓ 필터 B 저장 완료:")
    print(format_matrix(filter_b))

    section("[2] 패턴 입력")
    pattern = read_matrix("패턴")
    print("✓ 패턴 저장 완료:")
    print(format_matrix(pattern))

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    ms = (time_call_ms(mac, (pattern, filter_a)) + time_call_ms(mac, (pattern, filter_b))) / 2
    verdict = judge(score_a, score_b, "A", "B")

    section("[3] MAC 결과")
    print(f"A 점수: {fmt_score(score_a)}")
    print(f"B 점수: {fmt_score(score_b)}")
    print(f"연산 시간(평균/{REPEAT}회): {ms:.4f} ms")
    if verdict == UNDECIDED:
        print(f"판정: 판정 불가 (|A-B| < {EPSILON:g})")
    else:
        print(f"판정: {verdict}")

    section(f"[4] 성능 분석 (3×3, 평균/{REPEAT}회)")
    print_perf_table(measure_sizes([3]))
