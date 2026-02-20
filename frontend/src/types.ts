export interface InvestmentItem {
  name: string
  code: string
  expected_return?: number
  dividend_rate?: number
  payout_months?: number[]
  description: string
  allocation: number
  expected_annual_dividend?: number
  expected_quarterly_dividend?: number
}

export interface AssetCategory {
  category: string
  amount: number
  allocation_percent: number
  items: InvestmentItem[]
  expected_income?: number
}

export interface DetailedPlanResponse {
  monthly_goal: number
  total_allocation: number
  report: {
    current_assets: number
    expected_monthly_income: number
    monthly_goal_gap: number
    required_total_assets: number
    required_additional_assets: number
    weighted_annual_return: number
  }
  assets: AssetCategory[]
}
