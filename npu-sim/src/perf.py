import time
from src.matrix import make_matrix
from src.mac import mac

def measure_mac_ms():
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    print("-" * 40)

    # 잴 퍼즐 크기들 (3x3, 5x5, 13x13, 25x25)
    sizes = [3, 5, 13, 25]
    REPEAT = 10 # 미션 규칙에 따라 10번 반복해서 평균 내기!

    for n in sizes:
        # 시간 측정을 위해 크기에 맞는 가짜 퍼즐과 필터 만들기
        pattern = make_matrix(n, 1.0)
        filt = make_matrix(n, 1.0)
        
        elapsed = 0.0
        for _ in range(REPEAT):
            t0 = time.perf_counter() # 스톱워치 켜기
            mac(pattern, filt)       # 오직 연산 시간만 재요!
            elapsed += (time.perf_counter() - t0) # 스톱워치 끄고 시간 더하기
        
        # 밀리초(ms) 단위로 변환 후 평균 계산
        avg_ms = (elapsed / REPEAT) * 1000
        ops = n * n # 가로x세로 (연산 횟수)
        
        # 표 형식으로 출력
        print(f"{n}x{n:<8} {avg_ms:<15.4f} {ops}")