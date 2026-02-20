import { useState } from 'react'
import type { DetailedPlanResponse } from '../types'
import { downloadPdf, sendEmail } from '../utils/api'

interface ResultPageProps {
  result: DetailedPlanResponse
  onBack: () => void
  onReset: () => void
  onViewProjection: () => void
}

export default function ResultPage({ result, onBack, onReset, onViewProjection }: ResultPageProps) {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null)
  const [emailAddress, setEmailAddress] = useState<string>('')
  const [emailLoading, setEmailLoading] = useState<boolean>(false)
  const [emailSuccess, setEmailSuccess] = useState<string>('')

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

  const handleDownloadPdf = async () => {
    try {
      await downloadPdf(result)
    } catch (err) {
      alert('PDF 다운로드 중 오류가 발생했습니다.')
      console.error('PDF error:', err)
    }
  }

  const handleSendEmail = async () => {
    if (!emailAddress) {
      alert('이메일 주소를 입력하세요.')
      return
    }
    setEmailLoading(true)
    setEmailSuccess('')
    try {
      await sendEmail(emailAddress, result)
      setEmailSuccess('이메일이 성공적으로 발송되었습니다.')
      setEmailAddress('')
    } catch (err) {
      alert('이메일 전송 중 오류가 발생했습니다. SMTP 설정을 확인하세요.')
      console.error('Email error:', err)
    } finally {
      setEmailLoading(false)
    }
  }

  return (
    <section className="panel result-panel">
      <div className="panel-header">
        <div>
          <div className="hero-badge">HolinFlow</div>
          <h2>설계 결과</h2>
          <p>목표 달성을 위한 자산 배분과 추가 필요 금액을 확인하세요.</p>
        </div>
        <div className="panel-actions">
          <button className="btn-ghost" onClick={onBack}>뒤로가기</button>
          <button className="btn-ghost" onClick={onViewProjection}>수익 예측</button>
          <button className="btn-secondary" onClick={onReset}>다시 설계</button>
        </div>
      </div>

      <div className="result-container">
        <div className="summary-section">
          <h2>📈 설계 요약</h2>
          <div className="summary-stats">
            <div className="stat-card">
              <span className="stat-label">월수입 목표</span>
              <span className="stat-value">{result.monthly_goal.toLocaleString()}만원</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">현재 자산</span>
              <span className="stat-value">{Math.round(result.report.current_assets).toLocaleString()}만원</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">예상 월수입</span>
              <span className="stat-value">
                {result.report.expected_monthly_income.toFixed(1)}만원
              </span>
            </div>
            <div className="stat-card">
              <span className="stat-label">목표 부족액</span>
              <span className="stat-value">{result.report.monthly_goal_gap.toFixed(1)}만원</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">추가 필요 자산</span>
              <span className="stat-value">{result.report.required_additional_assets.toFixed(1)}만원</span>
            </div>
          </div>
        </div>

        <div className="report-export-section">
          <h2>📄 상세 리포트 생성</h2>
          <p className="report-description">
            추가 추천 종목(3개), 배당 상세 정보, AI 투자 의견 및 시장 의견이 포함된 PDF 리포트를 다운로드하거나 이메일로 받을 수 있습니다.
          </p>
          <div className="report-actions">
            <button className="btn-primary" onClick={handleDownloadPdf}>
              📥 PDF 다운로드
            </button>
            <div className="email-group">
              <input
                type="email"
                placeholder="이메일 주소"
                value={emailAddress}
                onChange={(e) => setEmailAddress(e.target.value)}
                className="email-input"
              />
              <button
                className="btn-primary"
                onClick={handleSendEmail}
                disabled={emailLoading}
              >
                {emailLoading ? '전송 중...' : '✉️ 이메일 발송'}
              </button>
            </div>
          </div>
          {emailSuccess && <div className="success-message">{emailSuccess}</div>}
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
                <div className="category-header-left">
                  <div className="category-info">
                    <h3>{asset.category}</h3>
                    <p className="category-details">
                      {asset.amount.toLocaleString()}만원 ({asset.allocation_percent.toFixed(1)}%)
                    </p>
                  </div>
                </div>
                <div className="category-header-right">
                  <div className="category-income">
                    <span className="income-label">예상 월 수익</span>
                    <span className="income-value">{asset.expected_income?.toFixed(1)}만원</span>
                  </div>
                  <span className="expand-icon">{expandedCategory === asset.category ? '▼' : '▶'}</span>
                </div>
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
                              {item.payout_months && item.payout_months.length > 0 && (
                                <div className="detail-row">
                                  <span>배당 지급월</span>
                                  <strong className="dividend-schedule">
                                    {item.payout_months.join(', ')}월
                                  </strong>
                                </div>
                              )}
                              {item.expected_quarterly_dividend !== undefined && (
                                <div className="detail-row">
                                  <span>예상 분기배당금</span>
                                  <strong className="dividend-amount">
                                    {item.expected_quarterly_dividend}만원
                                  </strong>
                                </div>
                              )}
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
    </section>
  )
}
