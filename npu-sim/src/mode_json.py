import json
from src.mac import mac
from src.judge import normalize_label, judge

def run_mode_2():
    print("\n#---------------------------------------")
    print("# [1] 필터 로드 및 데이터 분석")
    print("#---------------------------------------")
    
    # 1. 파일 읽어오기
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("오류: data.json 파일이 없습니다.")
        return
        
    filters = data.get("filters", {})
    patterns = data.get("patterns", {})
    
    total = passed = failed = 0
    
    # 2. 문제집(patterns)을 하나씩 꺼내서 풀기
    for key, p_data in patterns.items():
        total += 1
        print(f"\n--- {key} ---")
        
        input_pattern = p_data["input"]
        # 이상한 정답(+, x)을 깔끔한 표준 이름(Cross, X)으로 고치기 (라벨 정규화)
        expected = normalize_label(p_data["expected"])
        
        # 키 이름(size_3_1)에서 숫자 '3'을 뽑아내서 맞는 필터 찾기
        size_str = key.split('_')[1] 
        filter_key = f"size_{size_str}"
        cross_filter = filters[filter_key]["cross"]
        x_filter = filters[filter_key]["x"]
        
        # 3. MAC 연산으로 점수 내기
        score_cross = mac(input_pattern, cross_filter)
        score_x = mac(input_pattern, x_filter)
        
        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        
        # 4. 판정 및 PASS/FAIL 확인 (허용 오차 반영)
        verdict = judge(score_cross, score_x)
        
        if verdict == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
            
        print(f"판정: {verdict} | expected: {expected} | {status}")
        
    # 5. 최종 결과 요약
    print("\n#---------------------------------------")
    print("# [2] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")