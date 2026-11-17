from src.mac import mac
from src.mode_input import read_matrix
from src.mode_json import run_mode_2
from src.perf import measure_mac_ms

def run_mode_1():
    filter_a = read_matrix("필터 A")
    print("필터 A 저장 완료:", filter_a)
    
    filter_b = read_matrix("필터 B")
    print("필터 B 저장 완료:", filter_b)
    
    pattern = read_matrix("패턴")
    
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    
    print("\n[결과]")
    print(f"필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    
    if score_a > score_b:
        print("판정: A")
    elif score_b > score_a:
        print("판정: B")
    else:
        print("판정: 동점")

# 프로그램 실행
if __name__ == "__main__":
    print("===== Mini NPU Simulator =====")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("모드를 선택하세요 (1/2): ")

    if choice == '1':
        run_mode_1()
        measure_mac_ms() # 모드 1 끝나고 성능 분석 출력!
    elif choice == '2':
        run_mode_2()
        measure_mac_ms() # 모드 2 끝나고 성능 분석 출력!
    else:
        print("잘못된 입력입니다.")