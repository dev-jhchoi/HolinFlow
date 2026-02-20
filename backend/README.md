#  HolinFlow Backend

FastAPI 기반 AI 개인 금융 자동 설계 API 서버

##  목차
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [API 엔드포인트](#api-엔드포인트)
- [환경 설정](#환경-설정)

##  주요 기능

### 1. 자산 배분 계획 생성
- 월수입 목표, 현재 자산, 투자 성향 기반 최적 포트폴리오 계산
- 4대 자산 카테고리별 배분 (현금흐름, ETF, 배당주, REITs)
- 각 카테고리별 상세 투자 종목 추천
- 예상 수익률 및 배당금 계산

### 2. PDF 리포트 생성
- 한글 지원 PDF 문서 생성 (fpdf2 + malgun.ttf)  
- 추가 추천 종목 3개 포함
- 투자 성향별 AI 투자 의견
- 시장 전망 및 조언
- 배당 상세 정보 (지급월, 분기/연 배당금)

### 3. 이메일 발송
- SMTP를 통한 PDF 리포트 이메일 전송
- Gmail, Outlook 등 주요 메일 서비스 지원
- 환경변수 기반 보안 설정

##  기술 스택

- **FastAPI 0.115+** - 현대적인 Python 웹 프레임워크
- **Uvicorn** - ASGI 서버
- **fpdf2 2.7.9** - PDF 생성 라이브러리
- **Python 3.11+** - 최신 Python 기능 활용
- **SMTP** - 이메일 전송
- **Pydantic** - 데이터 검증

##  설치 및 실행

### 1. 의존성 설치
```bash
cd backend
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택사항)
이메일 기능을 사용하려면 `.env` 파일을 생성하세요:
```bash
cp .env.example .env
```

`.env` 파일 편집:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
SMTP_USE_TLS=true
```

### 3. 서버 실행
```bash
python main.py
```

서버가 http://localhost:8000 에서 실행됩니다.

### 4. API 문서 확인
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  API 엔드포인트

### `POST /api/plan-detailed`
자산 배분 계획 생성

**요청**:
```json
{
  "monthly_goal": 1000,
  "current_assets": 5000,
  "risk_level": "중립"
}
```

### `POST /api/report-pdf`
PDF 리포트 생성 및 다운로드

### `POST /api/report-email`
PDF 리포트 이메일 발송

##  환경 설정

### Gmail 앱 비밀번호 생성
1. Google 계정  보안  2단계 인증 활성화
2. 앱 비밀번호 생성  "메일" 선택
3. 생성된 16자리 비밀번호를 `.env`의 `SMTP_PASSWORD`에 입력

### 다른 메일 서비스

**Outlook**:
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

**Naver**:
```env
SMTP_HOST=smtp.naver.com
SMTP_PORT=587
```

##  테스트

PowerShell에서 API 테스트:
```powershell
$body = @{
    monthly_goal = 1000
    current_assets = 5000
    risk_level = '중립'
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post `
    -Uri http://localhost:8000/api/plan-detailed `
    -ContentType 'application/json' `
    -Body $body

$result.report
```

##  문제 해결

### 포트 8000 사용 중
```powershell
Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess | Stop-Process -Force
```

### fpdf2 한글 폰트 오류
Windows의 `C:\Windows\Fonts\malgun.ttf` 파일을 확인하세요.

##  라이센스

MIT License

---

**HolinFlow Backend** | FastAPI + Python 3.11+