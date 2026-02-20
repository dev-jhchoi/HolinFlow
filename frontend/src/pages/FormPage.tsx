interface FormPageProps {
  monthlyGoal: number
  currentAssets: number
  riskLevel: string
  loading: boolean
  error: string
  setMonthlyGoal: (value: number) => void
  setCurrentAssets: (value: number) => void
  setRiskLevel: (value: string) => void
  onSubmit: () => void
}

export default function FormPage({
  monthlyGoal,
  currentAssets,
  riskLevel,
  loading,
  error,
  setMonthlyGoal,
  setCurrentAssets,
  setRiskLevel,
  onSubmit
}: FormPageProps) {
  return (
    <section className="panel form-panel">
      <header className="hero">
        <div className="hero-badge">HolinFlow</div>
        <h1>AI 개인 금융 자동 설계</h1>
        <p className="subtitle">목표 수입과 현재 자산을 바탕으로 부족 금액까지 계산하고, 투자 성향에 맞는 포트폴리오를 제안합니다.</p>
        <div className="hero-highlights">
          <div className="highlight-card">
            <span className="highlight-icon">📊</span>
            <div>
              <span className="highlight-title">분석 항목</span>
              <strong className="highlight-value">4개 카테고리 분석</strong>
            </div>
          </div>
          <div className="highlight-card">
            <span className="highlight-icon">🧾</span>
            <div>
              <span className="highlight-title">리포트</span>
              <strong className="highlight-value">목표 부족액과 필요 자산</strong>
            </div>
          </div>
          <div className="highlight-card">
            <span className="highlight-icon">🧭</span>
            <div>
              <span className="highlight-title">추천 방식</span>
              <strong className="highlight-value">투자 성향 기반 제안</strong>
            </div>
          </div>
        </div>
      </header>
      <div className="form-container">
        <div className="form-group">
          <label>월수입 목표 (만원)</label>
          <input
            type="number"
            value={monthlyGoal}
            onChange={(e) => setMonthlyGoal(Number(e.target.value))}
            min="100"
          />
        </div>

        <div className="form-group">
          <label>현재 자산 (만원)</label>
          <input
            type="number"
            value={currentAssets}
            onChange={(e) => setCurrentAssets(Number(e.target.value))}
            min="0"
          />
        </div>

        <div className="form-group">
          <label>투자 성향</label>
          <select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)}>
            <option>보수적</option>
            <option>중립</option>
            <option>공격적</option>
          </select>
        </div>

        <button onClick={onSubmit} disabled={loading} className="btn-primary">
          {loading ? '계산 중...' : '설계 생성'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
    </section>
  )
}
