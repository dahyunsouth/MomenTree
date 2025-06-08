def classify_consumption(answers):
    # answers: 선택지 인덱스 리스트 [0, 2, 1, ...]
    save_score = answers.count(0) + answers.count(3)  # 저축/투자/가계부 등
    spend_score = answers.count(1) + answers.count(2)  # 쇼핑/외식/즉흥 등
    if save_score >= 5:
        return "절약형 소비자"
    elif spend_score >= 5:
        return "소비형 소비자"
    else:
        return "균형형 소비자"