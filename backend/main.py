from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import random

app = FastAPI()

# CORS 설정 (프론트엔드와 연동 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 데이터 모델 =====
class PlanRequest(BaseModel):
    monthly_goal: float
    current_assets: float
    risk_level: str

class InvestmentDetail(BaseModel):
    name: str
    code: str
    expected_return: float  # %
    risk_level: str
    description: str

class DividendStock(BaseModel):
    name: str
    code: str
    dividend_rate: float  # %
    annual_dividend: float  # 만원
    description: str

class AssetCategory(BaseModel):
    category: str
    amount: float
    allocation_percent: float
    items: List[Dict] = []
    expected_income: Optional[float] = None

class DetailedPlanResponse(BaseModel):
    monthly_goal: float
    total_allocation: float
    assets: List[AssetCategory]

# ===== 투자 상품 데이터베이스 =====
INVESTMENTS = {
    "low_risk": [
        {"name": "KODEX 200", "code": "069500", "expected_return": 6.5, "risk_level": "저위험", "description": "200대 기업 KOSPI 추종 ETF"},
        {"name": "미국 나스닥 100 ETF", "code": "QQQ", "expected_return": 9.2, "risk_level": "저위험", "description": "미국 기술주 중심 ETF"},
        {"name": "S&P 500 ETF", "code": "VOO", "expected_return": 7.8, "risk_level": "저위험", "description": "미국 대형주 500사 포함"},
    ],
    "mid_risk": [
        {"name": "KODEX 반도체", "code": "091160", "expected_return": 10.5, "risk_level": "중위험", "description": "반도체 업종 중심 ETF"},
        {"name": "KODEX 금융", "code": "122630", "expected_return": 9.0, "risk_level": "중위험", "description": "금융업종 ETF"},
        {"name": "이머징마켓 ETF", "code": "VWO", "expected_return": 11.2, "risk_level": "중위험", "description": "신흥국 주식 포트폴리오"},
    ],
    "high_risk": [
        {"name": "KODEX 바이오", "code": "091170", "expected_return": 15.8, "risk_level": "고위험", "description": "바이오·의료 기업 ETF"},
        {"name": "KODEX 에너지 화학", "code": "139290", "expected_return": 14.2, "risk_level": "고위험", "description": "에너지·화학 기업 중심"},
        {"name": "크립토 관련 ETF", "code": "GBTC", "expected_return": 18.5, "risk_level": "고위험", "description": "암호화폐 관련 자산"},
    ]
}

DIVIDEND_STOCKS = [
    {"name": "SK텔레콤", "code": "017670", "dividend_rate": 4.8, "annual_dividend": 2.4, "description": "통신업. 안정적 배당주"},
    {"name": "한국전력", "code": "015760", "dividend_rate": 5.2, "annual_dividend": 2.6, "description": "공기업. 높은 배당률"},
    {"name": "삼성전자", "code": "005930", "dividend_rate": 2.8, "annual_dividend": 5.0, "description": "대형주. 배당 및 성장성"},
    {"name": "NAVER", "code": "035420", "dividend_rate": 1.2, "annual_dividend": 3.2, "description": "기술주. 배당+성장"},
    {"name": "LG화학", "code": "051910", "dividend_rate": 3.5, "annual_dividend": 4.1, "description": "화학업. 안정적 배당"},
    {"name": "현대차", "code": "005380", "dividend_rate": 3.9, "annual_dividend": 5.5, "description": "자동차주. 배당+배당락익"},
]

REAL_ESTATE_PRODUCTS = [
    {"name": "신한 리츠", "code": "REITL", "expected_return": 7.2, "description": "부동산 투자신탁. 연 7-8% 배당"},
    {"name": "호텔신라 리츠", "code": "REITH", "expected_return": 6.8, "description": "리조트·호텔 REIT"},
    {"name": "부동산 펀드", "code": "REALPROP", "expected_return": 8.5, "description": "저평가 부동산 포트폴리오"},
]

CASH_PRODUCTS = [
    {"name": "정기예금 (연 4.5%)", "code": "DEPOSIT", "expected_return": 4.5, "description": "은행 정기예금. 원금안전"},
    {"name": "적금 (연 4.2%)", "code": "SAVINGS", "expected_return": 4.2, "description": "월 정액 납입식 적금"},
    {"name": "단기채권 펀드", "code": "BONDFUND", "expected_return": 4.8, "description": "저금리 채권 중심 펀드"},
]

# ===== API 엔드포인트 =====
@app.get("/")
def read_root():
    return {"message": "AI 개인 금융 자동 설계 API 서버 실행 중"}

@app.post("/api/plan", response_model=Dict)
def generate_plan(req: PlanRequest):
    """기본 자산 배분 계획 반환"""
    if req.risk_level == "공격적":
        allocation = {"현금흐름": 0.1, "투자": 0.5, "부동산": 0.2, "배당": 0.2}
    elif req.risk_level == "보수적":
        allocation = {"현금흐름": 0.4, "투자": 0.2, "부동산": 0.2, "배당": 0.2}
    else:
        allocation = {"현금흐름": 0.25, "투자": 0.35, "부동산": 0.2, "배당": 0.2}
    
    plan = {k: round(req.monthly_goal * v, 2) for k, v in allocation.items()}
    return {"allocation": plan}

@app.post("/api/plan-detailed", response_model=DetailedPlanResponse)
def generate_detailed_plan(req: PlanRequest):
    """상세 자산 배분 계획 + 종목 추천"""
    
    # 기본 배분 비율
    if req.risk_level == "공격적":
        allocation = {"현금흐름": 0.1, "투자": 0.5, "부동산": 0.2, "배당": 0.2}
        risk_category = "high_risk"
    elif req.risk_level == "보수적":
        allocation = {"현금흐름": 0.4, "투자": 0.2, "부동산": 0.2, "배당": 0.2}
        risk_category = "low_risk"
    else:
        allocation = {"현금흐름": 0.25, "투자": 0.35, "부동산": 0.2, "배당": 0.2}
        risk_category = "mid_risk"
    
    assets = []
    
    # 1. 현금흐름 (정기예금/적금 등)
    cash_amount = req.monthly_goal * allocation["현금흐름"]
    cash_items = random.sample(CASH_PRODUCTS, min(2, len(CASH_PRODUCTS)))
    cash_items = [
        {
            "name": item["name"],
            "code": item["code"],
            "expected_return": item["expected_return"],
            "description": item["description"],
            "allocation": round(cash_amount / len(cash_items), 0)
        }
        for item in cash_items
    ]
    assets.append(AssetCategory(
        category="현금흐름",
        amount=cash_amount,
        allocation_percent=allocation["현금흐름"] * 100,
        items=cash_items,
        expected_income=round(cash_amount * 4.5 / 100 / 12, 1)
    ))
    
    # 2. 투자 (ETF 등)
    investment_amount = req.monthly_goal * allocation["투자"]
    investment_items = random.sample(INVESTMENTS[risk_category], min(3, len(INVESTMENTS[risk_category])))
    investment_items = [
        {
            "name": item["name"],
            "code": item["code"],
            "expected_return": item["expected_return"],
            "description": item["description"],
            "allocation": round(investment_amount / len(investment_items), 0)
        }
        for item in investment_items
    ]
    assets.append(AssetCategory(
        category="투자 (ETF)",
        amount=investment_amount,
        allocation_percent=allocation["투자"] * 100,
        items=investment_items,
        expected_income=round(investment_amount * 10.0 / 100 / 12, 1)
    ))
    
    # 3. 배당 (배당주)
    dividend_amount = req.monthly_goal * allocation["배당"]
    dividend_items = random.sample(DIVIDEND_STOCKS, min(3, len(DIVIDEND_STOCKS)))
    dividend_items = [
        {
            "name": item["name"],
            "code": item["code"],
            "dividend_rate": item["dividend_rate"],
            "description": item["description"],
            "allocation": round(dividend_amount / len(dividend_items), 0),
            "expected_annual_dividend": round(
                (dividend_amount / len(dividend_items)) * item["dividend_rate"] / 100, 2
            )
        }
        for item in dividend_items
    ]
    assets.append(AssetCategory(
        category="배당주",
        amount=dividend_amount,
        allocation_percent=allocation["배당"] * 100,
        items=dividend_items,
        expected_income=round(dividend_amount * 3.8 / 100 / 12, 1)
    ))
    
    # 4. 부동산 (REITs)
    real_estate_amount = req.monthly_goal * allocation["부동산"]
    real_estate_items = random.sample(REAL_ESTATE_PRODUCTS, min(2, len(REAL_ESTATE_PRODUCTS)))
    real_estate_items = [
        {
            "name": item["name"],
            "code": item["code"],
            "expected_return": item["expected_return"],
            "description": item["description"],
            "allocation": round(real_estate_amount / len(real_estate_items), 0)
        }
        for item in real_estate_items
    ]
    assets.append(AssetCategory(
        category="부동산 (REITs)",
        amount=real_estate_amount,
        allocation_percent=allocation["부동산"] * 100,
        items=real_estate_items,
        expected_income=round(real_estate_amount * 7.5 / 100 / 12, 1)
    ))
    
    return DetailedPlanResponse(
        monthly_goal=req.monthly_goal,
        total_allocation=sum(a.amount for a in assets),
        assets=assets
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
