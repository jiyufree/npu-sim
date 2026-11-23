"""MAC(Multiply-Accumulate) 연산. 외부 라이브러리 없이 반복문으로 직접 구현한다."""


def mac(pattern, filt):
    """2차원 패턴과 필터를 같은 위치끼리 곱해 모두 더한 점수를 반환한다.

    크기 검증은 호출 전에 끝내는 것을 원칙으로 하지만,
    행 수가 다르면 잘못된 점수 대신 예외를 내도록 최소한으로 방어한다.
    """
    n = len(pattern)
    if n != len(filt):
        raise ValueError(f"크기 불일치: 패턴 {n}행, 필터 {len(filt)}행")
    total = 0.0
    for i in range(n):
        p_row = pattern[i]
        f_row = filt[i]
        for j in range(n):
            total += p_row[j] * f_row[j]
    return total


def mac_flat(pattern_flat, filt_flat):
    """(보너스) 1차원(길이 N²)으로 펼친 배열끼리의 MAC 연산.

    인덱스를 한 번만 계산하므로 2차원 접근보다 단순하다.
    """
    length = len(pattern_flat)
    if length != len(filt_flat):
        raise ValueError(f"길이 불일치: {length} vs {len(filt_flat)}")
    total = 0.0
    for k in range(length):
        total += pattern_flat[k] * filt_flat[k]
    return total
