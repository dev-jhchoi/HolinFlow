"""
planner.py - 금융 설계 로직
"""
class FinancialPlanner:
    def __init__(self, monthly_goal, current_assets, risk_level):
        self.monthly_goal = monthly_goal
        self.current_assets = current_assets
        self.risk_level = risk_level

    def generate_plan(self):
        # 간단한 예시: 자산 배분 비율 (현금흐름, 투자, 부동산, 배당)
        if self.risk_level == "공격적":
            allocation = {
                "현금흐름": 0.1,
                "투자": 0.5,
                "부동산": 0.2,
                "배당": 0.2
            }
        elif self.risk_level == "보수적":
            allocation = {
                "현금흐름": 0.4,
                "투자": 0.2,
                "부동산": 0.2,
                "배당": 0.2
            }
        else:  # 중립
            allocation = {
                "현금흐름": 0.25,
                "투자": 0.35,
                "부동산": 0.2,
                "배당": 0.2
            }
        # 목표 달성을 위한 월별 자산 배분
        plan = {k: round(self.monthly_goal * v, 2) for k, v in allocation.items()}
        return plan
