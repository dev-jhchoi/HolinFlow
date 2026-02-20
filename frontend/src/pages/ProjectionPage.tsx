import { useState } from 'react'
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { DetailedPlanResponse } from '../types'

interface ProjectionPageProps {
  result: DetailedPlanResponse
  onBackToResult: () => void
  onReset: () => void
}

export default function ProjectionPage({ result, onBackToResult, onReset }: ProjectionPageProps) {
  const [projectionYears, setProjectionYears] = useState<number>(10)

  const buildProjectionSeries = (data: DetailedPlanResponse, years: number) => {
    const annualRate = data.report.weighted_annual_return / 100
    const base = data.report.current_assets
    return Array.from({ length: years + 1 }, (_, index) => {
      const year = index
      const value = base * Math.pow(1 + annualRate, year)
      return { year, value }
    })
  }

  const formatWan = (value: number) => `${Number(value).toLocaleString()}만원`

  const series = buildProjectionSeries(result, projectionYears)
  const labelStep = Math.max(1, Math.ceil(series.length / 8))
  const chartData = series.map((point) => ({
    year: `${point.year}년`,
    value: Number(point.value.toFixed(0)),
  }))
  const yearTicks = chartData
    .filter((_, index) => index % labelStep === 0 || index === chartData.length - 1)
    .map((point) => point.year)

  return (
    <section className="panel projection-panel">
      <div className="panel-header">
        <div>
          <div className="hero-badge">HolinFlow</div>
          <h2>자산 성장 예측</h2>
          <p>현재 자산과 예상 수익률을 기준으로 연도별 자산 변화를 보여줍니다.</p>
        </div>
        <div className="panel-actions">
          <button className="btn-ghost" onClick={onBackToResult}>결과로 돌아가기</button>
          <button className="btn-secondary" onClick={onReset}>다시 설계</button>
        </div>
      </div>

      <div className="projection-controls">
        <label htmlFor="projectionYears">예측 기간</label>
        <div className="projection-range">
          <input
            id="projectionYears"
            type="range"
            min="3"
            max="30"
            step="1"
            value={projectionYears}
            onChange={(e) => setProjectionYears(Number(e.target.value))}
          />
          <span>{projectionYears}년</span>
        </div>
      </div>

      <div className="projection-chart">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 28, left: 4, bottom: 12 }}>
            <defs>
              <linearGradient id="projectionFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#1d4ed8" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="year"
              ticks={yearTicks}
              interval={0}
              tickMargin={8}
              padding={{ left: 4, right: 14 }}
              tick={{ fontSize: 11 }}
            />
            <YAxis
              width={90}
              tickMargin={8}
              tickFormatter={(value) => formatWan(Number(value))}
              tick={{ fontSize: 11 }}
            />
            <Tooltip
              formatter={(value) => formatWan(Number(value))}
              labelFormatter={(label) => label}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#1d4ed8"
              strokeWidth={3}
              fill="url(#projectionFill)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="projection-summary">
        <div>
          <span>연 기대수익률</span>
          <strong>{result.report.weighted_annual_return.toFixed(2)}%</strong>
        </div>
        <div>
          <span>현재 자산</span>
          <strong>{result.report.current_assets.toLocaleString()}만원</strong>
        </div>
        <div>
          <span>{projectionYears}년 후 예상</span>
          <strong>{formatWan(Math.round(buildProjectionSeries(result, projectionYears)[projectionYears].value))}</strong>
        </div>
      </div>
    </section>
  )
}
