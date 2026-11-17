EPSILON = 1e-9 # 아주아주 작은 허용 오차 기준

def normalize_label(raw):
    # 양옆 공백을 없애고 소문자로 바꿔서 비교해요
    key = str(raw).strip().lower()
    
    # +, cross, plus 라고 적혀있으면 모두 'Cross'로 통일!
    if key in ("+", "cross", "plus"):
        return "Cross"
    # x, ex 라고 적혀있으면 모두 'X'로 통일!
    if key in ("x", "ex"):
        return "X"
        
    return None # 모르는 글자면 빈값을 줘요

def judge(a, b, la="Cross", lb="X"):
    # 두 점수의 차이가 EPSILON(1e-9)보다 작으면 완전히 같은 점수(동점)로 봐줘요!
    if abs(a - b) < EPSILON:
        return "UNDECIDED"
    # 아니면 점수가 더 큰 쪽의 이름을 돌려줘요
    return la if a > b else lb