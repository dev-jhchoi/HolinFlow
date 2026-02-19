"""
models.py - 데이터 모델 정의 (확장용)
"""
# 현재는 단순 예시, 추후 사용자/포트폴리오 등 모델 확장 가능

class UserInput:
    def __init__(self, monthly_goal, current_assets, risk_level):
        self.monthly_goal = monthly_goal
        self.current_assets = current_assets
        self.risk_level = risk_level
