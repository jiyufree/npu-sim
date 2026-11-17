def parse_number(p):
    # 정수면 정수로, 소수점이면 실수로 변환하는 함수
    try:
        return int(p)
    except ValueError:
        return float(p)

def read_matrix(name, n=3):
    print(f"\n{name} ({n}x{n})를 한 줄씩 입력하세요. 예: 0 1 0")
    while True:
        rows = []
        ok = True
        for i in range(n):
            line = input(f"{i + 1}행: ")
            parts = line.split()
            
            # 입력 검증 1: 숫자를 3개 안 적었을 때
            if len(parts) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                ok = False
                break
            
            # 입력 검증 2: 숫자가 아닌 글자를 쳤을 때
            try:
                rows.append([parse_number(p) for p in parts])
            except ValueError:
                print("입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다.")
                ok = False
                break
        
        # 에러 없이 잘 입력됐으면 배열을 완성해서 돌려줌
        if ok:
            return rows