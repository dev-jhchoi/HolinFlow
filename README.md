#  HolinFlow - AI 개인 금융 자동 설계

> 월수입 목표를 입력하면 최적의 자산 배분 포트폴리오를 자동으로 설계하고, 상세한 투자 계획을 PDF 리포트로 제공하는 AI 기반 금융 설계 앱

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript)

##  주요 기능

###  자산 배분 자동 설계
- **투자 성향 기반 추천**: 보수적/중립/공격적 3가지 리스크 레벨
- **4대 자산 카테고리**: 현금흐름, ETF 투자, 배당주, 부동산(REITs)
- **상세 종목 추천**: 각 카테고리별 구체적인 투자 종목 및 배분액
- **목표 부족액 계산**: 월수입 목표 달성에 필요한 추가 자산 자동 계산

###  데이터 시각화
- **자산 배분 현황**: 카테고리별 배분 비율 및 예상 월 수익 표시
- **성장 예측 차트**: Recharts 기반 인터랙티브 자산 성장 시뮬레이션 (3~30년)
- **배당 스케줄**: 월별 배당 지급 일정 및 예상 배당금

###  리포트 생성
- **PDF 다운로드**: 상세 투자 계획서를 PDF로 다운로드
- **추가 추천 종목**: PDF에 3개의 추가 투자 아이템 포함
- **AI 의견**: 투자 성향별 맞춤 투자 조언
- **이메일 발송**: 생성된 PDF를 이메일로 전송

###  사용자 경험
- **반응형 디자인**: 모바일/태블릿/PC 모든 화면 크기 지원
- **모던 UI**: 그라디언트 효과, 애니메이션, 직관적인 네비게이션
- **실시간 계산**: 입력 즉시 최적 포트폴리오 생성

##  기술 스택

### Frontend
- **React 19** - 최신 React 기능 활용
- **Vite 8 (beta)** - 초고속 빌드 도구
- **TypeScript 5.6** - 타입 안정성
- **Recharts** - 데이터 시각화
- **CSS3** - 커스텀 스타일링

### Backend
- **FastAPI** - 고성능 Python 웹 프레임워크
- **fpdf2** - PDF 생성 (한글 지원)
- **Python 3.11+** - 최신 Python 기능 활용
- **SMTP** - 이메일 전송

##  빠른 시작

### 사전 요구사항
- Node.js 18+
- Python 3.11+
- npm 또는 yarn

### 1 저장소 클론
```bash
git clone https://github.com/yourusername/HolinFlow.git
cd HolinFlow
```

### 2 백엔드 실행
```bash
cd backend
pip install -r requirements.txt

# .env 파일 생성 (이메일 기능 사용 시)
cp .env.example .env
# .env 파일에서 SMTP 설정 입력

# 서버 실행
python main.py
```
백엔드가 http://localhost:8000 에서 실행됩니다.

### 3 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```
프론트엔드가 http://localhost:5173 에서 실행됩니다.

##  프로젝트 구조

```
HolinFlow/
 backend/                # FastAPI 백엔드
    main.py            # API 라우트 및 비즈니스 로직
    requirements.txt   # Python 의존성
    .env.example       # 환경변수 템플릿
    README.md          # 백엔드 상세 문서

 frontend/              # React 프론트엔드
    src/
       App.tsx       # 메인 앱 컴포넌트
       types.ts      # TypeScript 타입 정의
       pages/        # 페이지 컴포넌트
          FormPage.tsx       # 입력 폼
          ResultPage.tsx     # 결과 표시
          ProjectionPage.tsx # 자산 예측
       utils/        # 유틸리티 함수
           api.ts    # API 호출 함수
    package.json
    README.md          # 프론트엔드 상세 문서

 README.md              # 이 파일
```

##  API 엔드포인트

### `POST /api/plan-detailed`
자산 배분 계획 생성
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

자세한 API 문서: http://localhost:8000/docs

##  사용 방법

1. **월수입 목표 입력**: 원하는 월 수입 금액 (만원 단위)
2. **현재 자산 입력**: 현재 보유한 총 자산 (만원 단위)
3. **투자 성향 선택**: 보수적/중립/공격적 중 선택
4. **설계 생성 클릭**: AI가 최적의 자산 배분 계획 생성
5. **결과 확인**: 
   - 자산 배분 상세 내역
   - 예상 월 수익
   - 목표 달성에 필요한 추가 자산
6. **리포트 다운로드**: PDF 다운로드 또는 이메일 발송
7. **수익 예측 확인**: 장기 자산 성장 시뮬레이션

##  환경 설정

### 이메일 발송 설정 (선택사항)
`backend/.env` 파일 생성:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
SMTP_USE_TLS=true
```

Gmail 앱 비밀번호 생성:
1. Google 계정  보안  2단계 인증 활성화
2. 앱 비밀번호 생성  "메일" 선택
3. 생성된 16자리 비밀번호를 `SMTP_PASSWORD`에 입력

##  라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능

##  기여

이슈와 풀 리퀘스트를 환영합니다!

##  문의

프로젝트 관련 문의사항은 이슈를 등록해주세요.

---

Made with  by HolinFlow Team