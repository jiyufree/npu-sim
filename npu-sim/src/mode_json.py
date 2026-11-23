"""모드 2: data.json의 필터/패턴을 로드·검증하고 일괄 판정한다.

어떤 케이스에서 스키마/크기 문제가 생겨도 프로그램은 멈추지 않고
그 케이스만 FAIL(사유 포함)로 처리한다.
"""

import json
import re

from src.console import fmt_score, section
from src.judge import CROSS, UNDECIDED, X, judge, normalize_label
from src.mac import mac
from src.matrix import validate_square
from src.perf import REPEAT, measure_sizes, print_flat_compare, print_perf_table

FILTER_KEY_RE = re.compile(r"^size_(\d+)$")
PATTERN_KEY_RE = re.compile(r"^size_(\d+)_(\d+)$")


class CaseError(Exception):
    """케이스 하나를 FAIL로 처리해야 하는 데이터/스키마 문제."""


def load_json(path):
    """JSON 파일을 읽는다. 반환: (data, None) 또는 (None, 오류 메시지)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None, f"파일을 찾을 수 없습니다: {path}"
    except json.JSONDecodeError as e:
        return None, f"JSON 형식 오류 ({e.lineno}행 {e.colno}열): {e.msg}"
    except OSError as e:
        return None, f"파일을 읽을 수 없습니다: {e}"
    if not isinstance(data, dict):
        return None, "최상위 구조가 객체({...})가 아닙니다"
    return data, None


def load_filters(raw_filters):
    """filters 섹션을 {N: {"Cross": 행렬, "X": 행렬}} 형태로 정규화해 로드한다.

    필터 키('cross', 'x' 등)도 표준 라벨로 정규화한다.
    문제가 있는 필터는 건너뛰고 이유를 출력한다 (해당 크기 케이스는 나중에 FAIL).
    """
    filters = {}
    if not isinstance(raw_filters, dict):
        print("✗ 'filters' 섹션이 없거나 객체가 아닙니다")
        return filters

    for size_key, group in raw_filters.items():
        m = FILTER_KEY_RE.match(str(size_key))
        if not m:
            print(f"✗ {size_key}: 필터 키 형식 오류 (size_N 형태여야 함)")
            continue
        n = int(m.group(1))
        if not isinstance(group, dict):
            print(f"✗ {size_key}: 필터 묶음이 객체가 아닙니다")
            continue

        loaded = {}
        problems = []
        for label_key, matrix in group.items():
            label = normalize_label(label_key)
            if label is None:
                problems.append(f"알 수 없는 필터 라벨 '{label_key}'")
                continue
            size, err = validate_square(matrix)
            if err:
                problems.append(f"{label} 필터 {err}")
                continue
            if size != n:
                problems.append(f"{label} 필터 크기 {size}×{size} ≠ 키의 {n}×{n}")
                continue
            loaded[label] = matrix

        for label in (CROSS, X):
            if label not in loaded and not any(p.startswith(label) for p in problems):
                problems.append(f"{label} 필터 없음")

        if loaded:
            filters[n] = loaded
        mark = "✓" if not problems else "✗"
        names = ", ".join(lb for lb in (CROSS, X) if lb in loaded) or "없음"
        line = f"{mark} {size_key:<8}필터 로드 {'완료' if not problems else '일부 실패'} ({names})"
        if problems:
            line += " - " + "; ".join(problems)
        print(line)
    return filters


def evaluate_case(key, case, filters):
    """케이스 하나를 검증·판정한다. 문제가 있으면 CaseError를 던진다."""
    m = PATTERN_KEY_RE.match(str(key))
    if not m:
        raise CaseError("[스키마] 키 형식 오류 (size_N_idx 형태여야 함)")
    n = int(m.group(1))

    if not isinstance(case, dict):
        raise CaseError("[스키마] 케이스 값이 객체가 아닙니다")
    if "input" not in case:
        raise CaseError("[스키마] 'input' 항목 없음")
    if "expected" not in case:
        raise CaseError("[스키마] 'expected' 항목 없음")

    expected = normalize_label(case["expected"])
    if expected is None:
        raise CaseError(f"[라벨] 알 수 없는 expected 값 {case['expected']!r}")

    size, err = validate_square(case["input"])
    if err:
        raise CaseError(f"[스키마] input {err}")
    if size != n:
        raise CaseError(f"[크기] 패턴 {size}×{size} ≠ 키의 {n}×{n}")

    group = filters.get(n, {})
    missing = [lb for lb in (CROSS, X) if lb not in group]
    if missing:
        raise CaseError(f"[스키마] size_{n}의 {', '.join(missing)} 필터를 사용할 수 없음 (없거나 로드 실패)")

    score_cross = mac(case["input"], group[CROSS])
    score_x = mac(case["input"], group[X])
    return score_cross, score_x, judge(score_cross, score_x), expected


def run_mode_2(path):
    section("[1] 필터 로드")
    data, err = load_json(path)
    if err:
        print(f"✗ {err}")
        print("data.json 위치를 확인한 뒤 다시 실행하세요.")
        return
    filters = load_filters(data.get("filters"))

    section("[2] 패턴 분석 (라벨 정규화 적용)")
    patterns = data.get("patterns")
    if not isinstance(patterns, dict):
        print("✗ 'patterns' 섹션이 없거나 객체가 아닙니다")
        patterns = {}

    results = []  # (key, passed, reason)
    for key, case in patterns.items():
        print(f"--- {key} ---")
        try:
            score_cross, score_x, verdict, expected = evaluate_case(key, case, filters)
        except CaseError as e:
            print(f"FAIL ({e})")
            results.append((key, False, str(e)))
            continue
        except Exception as e:  # 예상 못 한 문제도 케이스 단위로 격리
            reason = f"[예외] {type(e).__name__}: {e}"
            print(f"FAIL ({reason})")
            results.append((key, False, reason))
            continue

        print(f"Cross 점수: {fmt_score(score_cross)}")
        print(f"X 점수: {fmt_score(score_x)}")
        if verdict == expected:
            print(f"판정: {verdict} | expected: {expected} | PASS")
            results.append((key, True, ""))
        elif verdict == UNDECIDED:
            reason = f"[동점] 동점(UNDECIDED) 처리 규칙에 따라 FAIL (expected: {expected})"
            print(f"판정: {verdict} | expected: {expected} | FAIL (동점 규칙)")
            results.append((key, False, reason))
        else:
            reason = f"[판정] 판정 {verdict} ≠ expected {expected}"
            print(f"판정: {verdict} | expected: {expected} | FAIL")
            results.append((key, False, reason))

    section(f"[3] 성능 분석 (평균/{REPEAT}회)")
    sizes = sorted({3, 5, 13, 25} | set(filters))
    rows = measure_sizes(sizes, filters)
    print_perf_table(rows)
    print()
    print("[보너스] 2D 접근 vs 1D(N²) 평탄화 접근")
    print_flat_compare(rows)

    section("[4] 결과 요약")
    passed = sum(1 for _, ok, _ in results if ok)
    failed = len(results) - passed
    print(f"총 테스트: {len(results)}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    if failed:
        print("\n실패 케이스:")
        for key, ok, reason in results:
            if not ok:
                print(f"- {key}: {reason}")
    print('\n(상세 원인 분석 및 복잡도 설명은 README.md의 "결과 리포트" 섹션 참고)')
