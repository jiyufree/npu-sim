"""n×n 2차원 행렬(패턴/필터) 데이터 구조와 검증 유틸리티."""


def make_matrix(n, fill=0):
    """n×n 크기의 2차원 리스트를 만든다."""
    return [[fill for _ in range(n)] for _ in range(n)]


def get_value(matrix, row, col):
    """특정 위치(row, col)의 값을 읽는다."""
    return matrix[row][col]


def set_value(matrix, row, col, value):
    """특정 위치(row, col)에 값을 저장한다."""
    matrix[row][col] = value


def is_number(value):
    # bool은 int의 하위 타입이라 True/False가 숫자로 통과하지 않도록 제외한다.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_square(matrix):
    """정사각 숫자 행렬인지 검사한다.

    반환: (크기 n, None) 또는 (None, 오류 메시지)
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        return None, "2차원 배열(list of list)이 아닙니다"
    n = len(matrix)
    for r, row in enumerate(matrix):
        if not isinstance(row, list):
            return None, f"{r + 1}행이 배열이 아닙니다"
        if len(row) != n:
            return None, f"정사각형이 아닙니다 (행 {n}개, {r + 1}행의 열 {len(row)}개)"
        for c, value in enumerate(row):
            if not is_number(value):
                return None, f"({r + 1},{c + 1}) 위치에 숫자가 아닌 값 {value!r}"
    return n, None


def flatten(matrix):
    """2차원 행렬을 길이 N²의 1차원 리스트로 변환한다 (보너스: 메모리 접근 최적화)."""
    flat = []
    for row in matrix:
        flat.extend(row)
    return flat


def format_matrix(matrix):
    """저장 확인용으로 행렬을 줄 단위 문자열로 만든다."""
    return "\n".join("  " + " ".join(str(v) for v in row) for row in matrix)
