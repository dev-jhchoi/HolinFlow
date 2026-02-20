import type { DetailedPlanResponse } from '../types'

const getAPIBaseUrl = (): string => {
  const hostname = window.location.hostname
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000'
  }
  if (hostname.includes('trycloudflare.com')) {
    return 'https://cook-boc-bbs-david.trycloudflare.com'
  }
  return `http://${hostname}:8000`
}

export const generatePlan = async (
  monthlyGoal: number,
  currentAssets: number,
  riskLevel: string
): Promise<DetailedPlanResponse> => {
  const apiUrl = `${getAPIBaseUrl()}/api/plan-detailed`
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
  return response.json()
}

export const downloadPdf = async (plan: DetailedPlanResponse): Promise<void> => {
  const apiUrl = `${getAPIBaseUrl()}/api/report-pdf`
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan })
  })
  if (!response.ok) throw new Error('PDF 생성 실패')
  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'HolinFlow_Report.pdf'
  a.click()
  window.URL.revokeObjectURL(url)
}

export const sendEmail = async (
  email: string,
  plan: DetailedPlanResponse
): Promise<void> => {
  const apiUrl = `${getAPIBaseUrl()}/api/report-email`
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, plan })
  })
  if (!response.ok) throw new Error('이메일 전송 실패')
}
