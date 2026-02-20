import { useState } from 'react'
import './App.css'
import type { DetailedPlanResponse } from './types'
import { generatePlan as apiGeneratePlan } from './utils/api'
import FormPage from './pages/FormPage'
import ResultPage from './pages/ResultPage'
import ProjectionPage from './pages/ProjectionPage'

function App() {
  const [monthlyGoal, setMonthlyGoal] = useState<number>(1000)
  const [currentAssets, setCurrentAssets] = useState<number>(5000)
  const [riskLevel, setRiskLevel] = useState<string>('중립')
  const [result, setResult] = useState<DetailedPlanResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  const [view, setView] = useState<'form' | 'result' | 'projection'>('form')

  const generatePlan = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await apiGeneratePlan(monthlyGoal, currentAssets, riskLevel)
      setResult(data)
      setView('result')
    } catch (err) {
      setError('백엔드 서버와 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    setView('form')
  }

  const handleReset = () => {
    setResult(null)
    setView('form')
  }

  const handleViewProjection = () => {
    setView('projection')
  }

  const handleBackToResult = () => {
    setView('result')
  }

  return (
    <div className="App">
      <div className={`app-shell ${view === 'result' ? 'is-result' : 'is-form'}`}>
        {view === 'form' && (
          <FormPage
            monthlyGoal={monthlyGoal}
            setMonthlyGoal={setMonthlyGoal}
            currentAssets={currentAssets}
            setCurrentAssets={setCurrentAssets}
            riskLevel={riskLevel}
            setRiskLevel={setRiskLevel}
            loading={loading}
            error={error}
            onSubmit={generatePlan}
          />
        )}

        {view === 'result' && result && (
          <ResultPage
            result={result}
            onBack={handleBack}
            onReset={handleReset}
            onViewProjection={handleViewProjection}
          />
        )}

        {view === 'projection' && result && (
          <ProjectionPage
            result={result}
            onBackToResult={handleBackToResult}
            onReset={handleReset}
          />
        )}
      </div>
    </div>
  )
}

export default App
