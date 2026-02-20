from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from email.message import EmailMessage
import io
import os
import random
import smtplib

try:
    from fpdf import FPDF
except ImportError:  # Fallback for environments without the dependency yet
    FPDF = None

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
    report: Dict
    assets: List[AssetCategory]

class ReportPdfRequest(BaseModel):
    plan: DetailedPlanResponse

class ReportEmailRequest(BaseModel):
    email: str
    plan: DetailedPlanResponse

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
    {"name": "SK텔레콤", "code": "017670", "dividend_rate": 4.8, "annual_dividend": 2.4, "payout_months": [3, 6, 9, 12], "description": "통신업. 안정적 배당주"},
    {"name": "한국전력", "code": "015760", "dividend_rate": 5.2, "annual_dividend": 2.6, "payout_months": [6, 12], "description": "공기업. 높은 배당률"},
    {"name": "삼성전자", "code": "005930", "dividend_rate": 2.8, "annual_dividend": 5.0, "payout_months": [3, 6, 9, 12], "description": "대형주. 배당 및 성장성"},
    {"name": "NAVER", "code": "035420", "dividend_rate": 1.2, "annual_dividend": 3.2, "payout_months": [4, 8, 12], "description": "기술주. 배당+성장"},
    {"name": "LG화학", "code": "051910", "dividend_rate": 3.5, "annual_dividend": 4.1, "payout_months": [4, 10], "description": "화학업. 안정적 배당"},
    {"name": "현대차", "code": "005380", "dividend_rate": 3.9, "annual_dividend": 5.5, "payout_months": [5, 11], "description": "자동차주. 배당+배당락익"},
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
    total_assets = req.current_assets
    category_rates = {
        "현금흐름": 4.5,
        "투자": 10.0,
        "배당": 3.8,
        "부동산": 7.5,
    }
    weighted_annual_return = (
        allocation["현금흐름"] * category_rates["현금흐름"]
        + allocation["투자"] * category_rates["투자"]
        + allocation["배당"] * category_rates["배당"]
        + allocation["부동산"] * category_rates["부동산"]
    )
    monthly_return_rate = weighted_annual_return / 100 / 12
    expected_monthly_income_raw = total_assets * monthly_return_rate if monthly_return_rate > 0 else 0.0
    required_total_assets_raw = req.monthly_goal / monthly_return_rate if monthly_return_rate > 0 else 0.0
    required_additional_assets_raw = max(0.0, required_total_assets_raw - total_assets)
    monthly_goal_gap_raw = max(0.0, req.monthly_goal - expected_monthly_income_raw)
    if monthly_goal_gap_raw < 0.01:
        monthly_goal_gap_raw = 0.0
        required_additional_assets_raw = 0.0

    expected_monthly_income = round(expected_monthly_income_raw, 2)
    required_total_assets = round(required_total_assets_raw, 2)
    required_additional_assets = round(required_additional_assets_raw, 2)
    monthly_goal_gap = round(monthly_goal_gap_raw, 2)
    
    # 1. 현금흐름 (정기예금/적금 등)
    cash_amount = total_assets * allocation["현금흐름"]
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
        expected_income=round(cash_amount * category_rates["현금흐름"] / 100 / 12, 1)
    ))
    
    # 2. 투자 (ETF 등)
    investment_amount = total_assets * allocation["투자"]
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
        expected_income=round(investment_amount * category_rates["투자"] / 100 / 12, 1)
    ))
    
    # 3. 배당 (배당주)
    dividend_amount = total_assets * allocation["배당"]
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
            ),
            "expected_quarterly_dividend": round(
                (dividend_amount / len(dividend_items)) * item["dividend_rate"] / 100 / 4, 2
            ),
            "payout_months": item["payout_months"],
        }
        for item in dividend_items
    ]
    assets.append(AssetCategory(
        category="배당주",
        amount=dividend_amount,
        allocation_percent=allocation["배당"] * 100,
        items=dividend_items,
        expected_income=round(dividend_amount * category_rates["배당"] / 100 / 12, 1)
    ))
    
    # 4. 부동산 (REITs)
    real_estate_amount = total_assets * allocation["부동산"]
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
        expected_income=round(real_estate_amount * category_rates["부동산"] / 100 / 12, 1)
    ))
    
    return DetailedPlanResponse(
        monthly_goal=req.monthly_goal,
        total_allocation=sum(a.amount for a in assets),
        report={
            "current_assets": total_assets,
            "expected_monthly_income": expected_monthly_income,
            "monthly_goal_gap": monthly_goal_gap,
            "required_total_assets": required_total_assets,
            "required_additional_assets": required_additional_assets,
            "weighted_annual_return": round(weighted_annual_return, 2),
        },
        assets=assets
    )

def _pick_extra_recommendations(existing_codes: set, count: int = 3) -> List[Dict]:
    pool: List[Dict] = []
    for items in INVESTMENTS.values():
        for item in items:
            pool.append({
                "name": item["name"],
                "code": item["code"],
                "type": "ETF",
                "description": item["description"],
            })
    for item in DIVIDEND_STOCKS:
        pool.append({
            "name": item["name"],
            "code": item["code"],
            "type": "배당주",
            "description": item["description"],
        })
    for item in REAL_ESTATE_PRODUCTS:
        pool.append({
            "name": item["name"],
            "code": item["code"],
            "type": "REITs",
            "description": item["description"],
        })
    for item in CASH_PRODUCTS:
        pool.append({
            "name": item["name"],
            "code": item["code"],
            "type": "현금성",
            "description": item["description"],
        })

    candidates = [item for item in pool if item["code"] not in existing_codes]
    if len(candidates) <= count:
        return candidates
    return random.sample(candidates, count)

def _build_ai_opinion(risk_level: str) -> str:
    if risk_level == "공격적":
        return "공격적 성향은 성장성 섹터의 변동성을 감내하는 대신 기대수익을 높입니다. 분기 리밸런싱으로 리스크를 관리하세요."
    if risk_level == "보수적":
        return "보수적 성향은 안정적인 현금흐름을 우선합니다. 수익률은 낮지만 변동성 방어에 유리합니다."
    return "중립 성향은 성장과 안정의 균형을 목표로 합니다. ETF/배당/현금성 비중을 고르게 유지하세요."

def _build_market_opinion() -> str:
    return "현재 시장은 금리 민감도가 높아 변동성이 반복될 수 있습니다. 배당/현금흐름 비중을 유지하며 분산 투자가 유효합니다."

def _get_pdf_font(pdf: "FPDF") -> str:
    font_path = "C:/Windows/Fonts/malgun.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Malgun", "", font_path, uni=True)
        return "Malgun"
    return "Helvetica"

def _build_report_pdf(plan: DetailedPlanResponse) -> bytes:
    if FPDF is None:
        raise HTTPException(status_code=500, detail="PDF 생성 라이브러리가 설치되지 않았습니다.")

    existing_codes = {
        item.get("code")
        for asset in plan.assets
        for item in asset.items
        if isinstance(item, dict)
    }
    extra_items = _pick_extra_recommendations(existing_codes, count=3)
    ai_opinion = _build_ai_opinion(str(plan.report.get("risk_level", "중립")))
    market_opinion = _build_market_opinion()

    pdf = FPDF()
    pdf.add_page()
    font_name = _get_pdf_font(pdf)
    pdf.set_font(font_name, size=12)

    pdf.cell(0, 10, "HolinFlow Detailed Report", ln=True)
    pdf.set_font(font_name, size=10)
    pdf.cell(0, 8, f"Monthly Goal: {plan.monthly_goal} 만원", ln=True)
    pdf.cell(0, 8, f"Current Assets: {plan.report.get('current_assets', 0)} 만원", ln=True)
    pdf.cell(0, 8, f"Expected Monthly Income: {plan.report.get('expected_monthly_income', 0)} 만원", ln=True)
    pdf.cell(0, 8, f"Required Additional Assets: {plan.report.get('required_additional_assets', 0)} 만원", ln=True)

    pdf.ln(4)
    pdf.set_font(font_name, size=11)
    pdf.cell(0, 8, "Allocation Details", ln=True)
    pdf.set_font(font_name, size=9)
    for asset in plan.assets:
        pdf.cell(0, 7, f"- {asset.category} ({round(asset.amount, 1)} 만원)", ln=True)
        for item in asset.items:
            name = item.get("name", "")
            code = item.get("code", "")
            allocation = item.get("allocation", 0)
            pdf.cell(0, 6, f"  * {name} ({code}) / {allocation} 만원", ln=True)
            payout_months = item.get("payout_months")
            if payout_months:
                count = len(payout_months)
                months_text = ", ".join(str(month) for month in payout_months)
                pdf.cell(0, 6, f"    - Dividend: {count}x / {months_text}월", ln=True)

    pdf.ln(3)
    pdf.set_font(font_name, size=11)
    pdf.cell(0, 8, "Additional Recommendations (3)", ln=True)
    pdf.set_font(font_name, size=9)
    for item in extra_items:
        pdf.multi_cell(0, 6, f"- {item['name']} ({item['code']}) [{item['type']}] {item['description']}")

    pdf.ln(2)
    pdf.set_font(font_name, size=11)
    pdf.cell(0, 8, "AI Opinion", ln=True)
    pdf.set_font(font_name, size=9)
    pdf.multi_cell(0, 6, ai_opinion)

    pdf.set_font(font_name, size=11)
    pdf.cell(0, 8, "Market Opinion", ln=True)
    pdf.set_font(font_name, size=9)
    pdf.multi_cell(0, 6, market_opinion)

    return bytes(pdf.output())

def _send_email_with_pdf(to_email: str, pdf_bytes: bytes) -> None:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user or "")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_host or not smtp_from:
        raise HTTPException(status_code=500, detail="SMTP 설정이 필요합니다.")

    message = EmailMessage()
    message["Subject"] = "HolinFlow 상세 리포트"
    message["From"] = smtp_from
    message["To"] = to_email
    message.set_content("첨부된 PDF 파일에서 상세 리포트를 확인하세요.")
    message.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename="HolinFlow_Report.pdf")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if use_tls:
            server.starttls()
        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)
        server.send_message(message)

@app.post("/api/report-pdf")
def create_report_pdf(payload: ReportPdfRequest):
    pdf_bytes = _build_report_pdf(payload.plan)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=HolinFlow_Report.pdf"},
    )

@app.post("/api/report-email")
def send_report_email(payload: ReportEmailRequest):
    if "@" not in payload.email:
        raise HTTPException(status_code=400, detail="이메일 형식을 확인하세요.")
    pdf_bytes = _build_report_pdf(payload.plan)
    _send_email_with_pdf(payload.email, pdf_bytes)
    return {"status": "sent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
