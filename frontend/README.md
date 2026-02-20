#  HolinFlow Frontend

React 19 + Vite 8 + TypeScript 기반 AI 개인 금융 자동 설계 웹 애플리케이션

##  목차
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [프로젝트 구조](#프로젝트-구조)
- [컴포넌트 설명](#컴포넌트-설명)

##  주요 기능

###  입력 폼 (FormPage)
- 월수입 목표 입력
- 현재 자산 입력
- 투자 성향 선택 (보수적/중립/공격적)
- 실시간 유효성 검증

###  결과 표시 (ResultPage)
- **설계 요약**: 5가지 핵심 지표 카드
- **자산 배분 상세**: 카테고리별 확장 가능한 카드
- **PDF 리포트 생성**: 다운로드 + 이메일 발송
- **투자 조언**: 5가지 실용적인 투자 팁

###  자산 예측 (ProjectionPage)
- Recharts 기반 인터랙티브 차트
- 3~30년 자산 성장 시뮬레이션
- 슬라이더로 예측 기간 조정

##  기술 스택

- **React 19** - 최신 React 기능
- **Vite 8 (beta)** - 초고속 빌드 도구
- **TypeScript 5.6** - 타입 안정성
- **Recharts** - 차트 라이브러리
- **CSS3** - 모던 CSS

##  설치 및 실행

### 1. 의존성 설치
```bash
cd frontend
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```
브라우저에서 http://localhost:5173 으로 접속

### 3. 네트워크 접근 (선택)
```bash
npm run dev -- --host
```

### 4. 프로덕션 빌드
```bash
npm run build
```

##  프로젝트 구조

```
frontend/
 src/
    App.tsx         # 메인 앱 컴포넌트 (89줄)
    App.css         # 메인 스타일시트
    types.ts        # TypeScript 타입 정의
    pages/          # 페이지 컴포넌트
       FormPage.tsx       # 입력 폼
       ResultPage.tsx     # 결과 표시
       ProjectionPage.tsx # 자산 예측
    utils/          # 유틸리티 함수
        api.ts      # API 호출 함수
 package.json
 vite.config.ts
```

##  컴포넌트 설명

### `App.tsx`
메인 애플리케이션 컴포넌트 (상태 관리 및 페이지 조합)

**주요 상태**:
```typescript
const [monthlyGoal, setMonthlyGoal] = useState<number>(1000)
const [currentAssets, setCurrentAssets] = useState<number>(5000)
const [riskLevel, setRiskLevel] = useState<string>('중립')
const [result, setResult] = useState<DetailedPlanResponse | null>(null)
const [view, setView] = useState<'form' | 'result' | 'projection'>('form')
```

### `pages/FormPage.tsx`
사용자 입력 폼 (Hero 섹션, 입력 필드, 제출 버튼)

### `pages/ResultPage.tsx`
자산 배분 결과 표시 및 리포트 생성

### `pages/ProjectionPage.tsx`
자산 성장 예측 차트 (Recharts)

### `types.ts`
TypeScript 타입 정의
- `InvestmentItem`
- `AssetCategory`
- `DetailedPlanResponse`

### `utils/api.ts`
API 통신 유틸리티
- `getAPIBaseUrl()`
- `generatePlan()`
- `downloadPdf()`
- `sendEmail()`

##  스타일링

- **CSS Variables**: 색상, 간격, 폰트 일관성
- **Flexbox & Grid**: 레이아웃
- **Media Queries**: 반응형 디자인

##  API 통신

```typescript
// 자산 배분 계획 생성
const result = await generatePlan(1000, 5000, '중립')

// PDF 다운로드
await downloadPdf(result)

// 이메일 발송
await sendEmail('user@example.com', result)
```

##  반응형 디자인

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

##  문제 해결

### 포트 5173 사용 중
```powershell
Get-Process -Name node | Stop-Process -Force
```

### TypeScript 오류
```bash
rm -rf node_modules package-lock.json
npm install
```

##  라이센스

MIT License

---

**HolinFlow Frontend** | React 19 + Vite 8 + TypeScript 5.6