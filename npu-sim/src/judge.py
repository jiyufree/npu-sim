"""라벨 정규화와 epsilon 기반 점수 비교(판정) 정책."""

EPSILON = 1e-9  # |A - B| < EPSILON 이면 동점으로 본다

CROSS = "Cross"
X = "X"
UNDECIDED = "UNDECIDED"

# 외부 데이터에 쓰이는 다양한 표기 → 프로그램 내부 표준 라벨
_LABEL_MAP = {
    "+": CROSS,
    "cross": CROSS,
    "plus": CROSS,
    "x": X,
    "ex": X,
    "×": X,
}


def normalize_label(raw):
    """'+', 'cross', 'x' 등 표기를 표준 라벨(Cross / X)로 바꾼다. 모르는 값이면 None."""
    if raw is None:
        return None
    key = str(raw).strip().lower()
    return _LABEL_MAP.get(key)


def is_tie(score_a, score_b, eps=EPSILON):
    return abs(score_a - score_b) < eps


def judge(score_a, score_b, label_a=CROSS, label_b=X, eps=EPSILON):
    """두 점수를 비교해 더 큰 쪽의 라벨을, 차이가 eps 미만이면 UNDECIDED를 반환한다."""
    if is_tie(score_a, score_b, eps):
        return UNDECIDED
    return label_a if score_a > score_b else label_b
