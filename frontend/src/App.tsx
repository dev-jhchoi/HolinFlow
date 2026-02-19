import { useState } from 'react'
import './App.css'

interface InvestmentItem {
  name: string
  code: string
  expected_return?: number
  dividend_rate?: number
  description: string
  allocation: number
  expected_annual_dividend?: number
}

interface AssetCategory {
  category: string
  amount: number
  allocation_percent: number
  items: InvestmentItem[]
  expected_income?: number
}

interface DetailedPlanResponse {
  monthly_goal: number
  total_allocation: number
  assets: AssetCategory[]
}

function App() {
  const [monthlyGoal, setMonthlyGoal] = useState<number>(1000)
  const [currentAssets, setCurrentAssets] = useState<number>(5000)
  const [riskLevel, setRiskLevel] = useState<string>('중립')
  const [result, setResult] = useState<DetailedPlanResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null)

  // API 기본 URL 동적 설정 (로컬/네트워크/외부 IP 자동 감지)
  const getAPIBaseUrl = (): string => {
    const hostname = window.location.hostname
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000'
    }
    // 다른 IP/도메인인 경우 같은 호스트의 8000 포트 사용
    return `http://${hostname}:8000`
  }

  const generatePlan = async () => {
    setLoading(true)
    setError('')
    try {
      const apiUrl = `${getAPIBaseUrl()}/api/plan-detailed`
      console.log('API URL:', apiUrl) // 디버깅용
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          monthly_goal: monthlyGoal,
          current_assets: currentAssets,
          risk_level: riskLevel
        })
      })
      if (!response.ok) throw new Error('API 오류')
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('백엔드 서버와 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getCategoryColor = (category: string): string => {
    const colors: { [key: string]: string } = {
      '현금흐름': '#4CAF50',
      '투자 (ETF)': '#2196F3',
      '배당주': '#FF9800',
      '부동산 (REITs)': '#9C27B0'
    }
    return colors[category] || '#667eea'
  }

  const toggleCategory = (category: string) => {
    setExpandedCategory(expandedCategory === category ? null : category)
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>💰📊 AI 개인 금융 자동 설계</h1>
        <p className="subtitle">월수입 목표를 입력하면 최적의 자산 배분을 제안합니다</p>
        
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
          
          <button onClick={generatePlan} disabled={loading} className="btn-generate">
            {loading ? '계산 중...' : '설계 생성'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        {result && (
          <div className="result-container">
            <div className="summary-section">
              <h2>📈 설계 요약</h2>
              <div className="summary-stats">
                <div className="stat-card">
                  <span className="stat-label">월수입 목표</span>
                  <span className="stat-value">{result.monthly_goal.toLocaleString()}만원</span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">총 배분액</span>
                  <span className="stat-value">{Math.round(result.total_allocation).toLocaleString()}만원</span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">예상 월수입</span>
                  <span className="stat-value">
                    {(result.assets.reduce((sum, a) => sum + (a.expected_income || 0), 0)).toFixed(1)}만원
                  </span>
                </div>
              </div>
            </div>

            <div className="allocation-section">
              <h2>🎯 자산 배분 상세</h2>
              {result.assets.map((asset) => (
                <div key={asset.category} className="asset-category-card">
                  <div 
                    className="category-header"
                    onClick={() => toggleCategory(asset.category)}
                    style={{ borderLeftColor: getCategoryColor(asset.category) }}
                  >
                    <div className="category-info">
                      <h3>{asset.category}</h3>
                      <p className="category-details">
                        {asset.amount.toLocaleString()}만원 ({asset.allocation_percent.toFixed(1)}%)
                      </p>
                    </div>
                    <div className="category-income">
                      <span className="income-label">예상 월 수익</span>
                      <span className="income-value">{asset.expected_income?.toFixed(1)}만원</span>
                    </div>
                    <span className="expand-icon">{expandedCategory === asset.category ? '▼' : '▶'}</span>
                  </div>

                  {expandedCategory === asset.category && (
                    <div className="category-details-section">
                      <div className="items-grid">
                        {asset.items.map((item, idx) => (
                          <div key={idx} className="item-card">
                            <div className="item-header">
                              <h4>{item.name}</h4>
                              <span className="item-code">{item.code}</span>
                            </div>
                            <p className="item-description">{item.description}</p>
                            <div className="item-details">
                              <div className="detail-row">
                                <span>배분액</span>
                                <strong>{item.allocation.toLocaleString()}만원</strong>
                              </div>
                              {item.expected_return && (
                                <div className="detail-row">
                                  <span>예상수익률</span>
                                  <strong className="return-positive">{item.expected_return}%</strong>
                                </div>
                              )}
                              {item.dividend_rate && (
                                <>
                                  <div className="detail-row">
                                    <span>배당률</span>
                                    <strong className="dividend-positive">{item.dividend_rate}%</strong>
                                  </div>
                                  <div className="detail-row">
                                    <span>예상 연배당금</span>
                                    <strong className="dividend-amount">{item.expected_annual_dividend}만원</strong>
                                  </div>
                                </>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="recommendation-section">
              <h2>💡 투자 조언</h2>
              <ul className="advice-list">
                <li>📌 월 수익 목표 달성을 위해 추천된 배분 비율을 준수하세요</li>
                <li>📊 시장 변동성에 따라 분기별 리밸런싱을 권장합니다</li>
                <li>🔄 배당주는 매년 배당금 재투자로 복리 효과를 누릴 수 있습니다</li>
                <li>⚠️ ETF 투자 시 환율 변동성을 고려하세요 (해외 자산 비중 시)</li>
                <li>📈 정기적인 수익 점검으로 목표 달성도를 추적하세요</li>
              </ul>
            </div>
          </div>
        )}
      </header>
    </div>
  )
}

export default App
