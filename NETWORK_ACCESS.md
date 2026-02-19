# 🌐 네트워크 접속 가이드

## 현재 서버 정보

### 로컬 주소
- **프론트엔드**: http://localhost:5173
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

### 로컬 네트워크 주소 (같은 와이파이/LAN)
```
프론트엔드 (Vite):   http://192.168.123.103:5173
백엔드 API (FastAPI): http://192.168.123.103:8000
API 문서:             http://192.168.123.103:8000/docs
```

### 외부 인터넷 접속 (다른 네트워크)
공인 IP를 통한 접속 (라우터 포트 포워딩 필요):
```
프론트엔드: http://58.29.48.214:5173
백엔드 API: http://58.29.48.214:8000
```

---

## 🔧 외부 접속 설정 (3가지 방법)

### 방법 1️⃣: Windows 방화벽 개방 (권장)

**Windows+X** → **Windows Terminal(관리자)** 또는 **PowerShell(관리자)** 실행

```powershell
# 포트 5173 개방 (프론트엔드)
New-NetFirewallRule -DisplayName "HolinFlow-Frontend" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5173

# 포트 8000 개방 (백엔드 API)
New-NetFirewallRule -DisplayName "HolinFlow-API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
```

#### ✅ 확인 방법
```powershell
# 규칙 확인
Get-NetFirewallRule -DisplayName "HolinFlow-*"
```

---

### 방법 2️⃣: 라우터 포트 포워딩 (영구적)

1. **라우터 관리 페이지 접속**
   - 주소: http://192.168.1.1 또는 http://192.168.0.1
   - 기본 로그인: admin/admin (또는 라우터 뒷면 확인)

2. **포트 포워딩 설정**
   
   | 규칙명 | 프로토콜 | WAN 포트 | LAN IP | LAN 포트 |
   |--------|---------|---------|--------|---------|
   | HolinFlow-Frontend | TCP | 5173 | 192.168.123.103 | 5173 |
   | HolinFlow-API | TCP | 8000 | 192.168.123.103 | 8000 |

3. **저장 & 재부팅**

#### ✅ 확인 방법
다른 네트워크(모바일 핫스팟 등)에서 접속 시도:
```
http://58.29.48.214:5173
http://58.29.48.214:8000
```

---

### 방법 3️⃣: ngrok 터널링 (임시/무료)

```bash
# 1. ngrok 설치
npm install -g ngrok

# 2. ngrok 계정 생성 (https://dashboard.ngrok.com)

# 3. 터미널 1: 프론트엔드 터널
ngrok http 5173

# 4. 터미널 2: 백엔드 터널 (다른 터미널 열기)
ngrok http 8000
```

#### 🔗 ngrok 공개 URL 예시
```
프론트엔드: https://abc123def-45.ngrok.io → localhost:5173
백엔드:     https://xyz789ghi-45.ngrok.io → localhost:8000
```

**주의**: ngrok URL은 세션마다 변경됨

---

## 🧪 접속 테스트

### 방법 A: 같은 네트워크 테스트
```bash
# 같은 와이파이 다른 기기에서 (예: 스마트폰)
http://192.168.123.103:5173
```

### 방법 B: 다른 네트워크 테스트
```bash
# 모바일 핫스팟 또는 다른 와이파이에서
http://58.29.48.214:5173
```

### 방법 C: API 요청 테스트
```bash
# 프론트에서 API 호출 시 다음 URL 사용
POST http://58.29.48.214:8000/api/plan-detailed
```

---

## ⚠️ 주의사항

### 1️⃣ 라우터 재부팅 후 공인 IP 변경 가능
- 공인 IP 고정: ISP에 문의하거나 유료 서비스 가입
- 현재 공인 IP: **58.29.48.214** (세션마다 변경 가능)

### 2️⃣ 보안 고려사항
- ⚠️ **HTTP 사용 (HTTPS 아님)**: 본인 네트워크 테스트용만 권장
- ⚠️ **CORS 조건 필요**: 프론트가 다른 도메인 API 호출 시 CORS 설정 필수

### 3️⃣ 프론트엔드에서 백엔드 URL 설정
현재 [frontend/src/App.tsx](frontend/src/App.tsx)의 API 호출 부분:
```typescript
// 로컬 개발용
const response = await fetch('http://localhost:8000/api/plan-detailed', {...})

// 외부 접속 시 변경 필요
const response = await fetch('http://58.29.48.214:8000/api/plan-detailed', {...})
```

**자동 감지 코드 (권장):**
```typescript
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : `http://${window.location.hostname}:8000`;

const response = await fetch(`${API_BASE_URL}/api/plan-detailed`, {...})
```

---

## 🚀 완벽한 외부 접속 설정 단계별 가이드

### Step 1: 백엔드 실행 (포트 8000)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 2: 프론트엔드 실행 (포트 5173)  
```bash
cd frontend
npm run dev -- --host
```

### Step 3: Windows 방화벽 개방
```powershell
# 관리자 PowerShell에서
New-NetFirewallRule -DisplayName "HolinFlow-Frontend" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5173
New-NetFirewallRule -DisplayName "HolinFlow-API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
```

### Step 4: 라우터 포트 포워딩 (공인 IP 접속용)
- 라우터 설정 → 포트 포워딩
- 5173, 8000 포트를 192.168.123.103으로 포워딩

### Step 5: 접속 테스트
```
같은 네트워크:  http://192.168.123.103:5173
다른 네트워크:  http://58.29.48.214:5173
```

---

## 📊 접속 방식 비교

| 방식 | 같은 네트워크 | 다른 네트워크 | 설정 | 보안 | 비용 |
|------|-----------|-----------|------|------|------|
| **localhost** | ✅ | ❌ | 매우 쉬움 | ✅ 최고 | 무료 |
| **로컬 IP** | ✅ | ❌ | 쉬움 | ✅ 높음 | 무료 |
| **방화벽 개방** | ✅ | ✅ | 중간 | ⚠️ 중간 | 무료 |
| **포트 포워딩** | ✅ | ✅ | 어려움 | ✅ 높음 | 무료 |
| **ngrok** | ✅ | ✅ | 쉬움 | ⚠️ 중간 | 무료/유료 |
| **클라우드 배포** | ✅ | ✅ | 어려움 | ✅ 최고 | 유료 |

---

## 🌍 권장 배포 방법

### 1. 로컬 테스트 (현재)
```
192.168.123.103:5173 / :8000
```

### 2. 임시 외부 공유
```
ngrok 또는 포트 포워딩 + 58.29.48.214
```

### 3. 장기 배포 (권장)
```
AWS EC2 / Heroku / Azure App Service 등에 배포
→ 고정 도메인 및 HTTPS 보안
```

---

**마지막 업데이트**: 2026년 2월  
**공인 IP**: 58.29.48.214 (임시 정보, 라우터 재부팅 시 변경 가능)
