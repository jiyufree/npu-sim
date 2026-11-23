"""콘솔 출력/입력 공통 함수."""

import sys


def section(title):
    line = "#" + "-" * 39
    print()
    print(line)
    print(f"# {title}")
    print(line)


def ask(prompt):
    """input() 래퍼. 입력 스트림이 끝나면(EOF/Ctrl+D) 안내 후 정상 종료한다."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 종료되어 프로그램을 마칩니다.")
        sys.exit(0)


def fmt_score(score):
    """점수를 float로 통일해 출력한다 (예: 5 → 5.0, 0.8999999999999999 그대로)."""
    return repr(float(score))
