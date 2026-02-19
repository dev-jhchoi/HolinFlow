"""
main.py - AI 기반 개인 금융 자동 설계 앱 진입점
"""
from planner import FinancialPlanner

def main():
    print("=== AI 개인 금융 자동 설계 ===")
    monthly_goal = float(input("월수입 목표(만원): "))
    current_assets = float(input("현재 자산(만원): "))
    risk_level = input("투자 성향(보수적/중립/공격적): ")

    planner = FinancialPlanner(monthly_goal, current_assets, risk_level)
    plan = planner.generate_plan()

    print("\n[자동 설계 결과]")
    for k, v in plan.items():
        print(f"{k}: {v}만원")

if __name__ == "__main__":
    main()
