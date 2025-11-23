import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ExpenseList from './pages/ExpenseList'
import IncomeList from './pages/IncomeList'
import BudgetList from './pages/BudgetList'
import GoalList from './pages/GoalList'
import ExpenseDetail from './pages/ExpenseDetail'
import BudgetDetail from './pages/BudgetDetail'
import IncomeDetail from './pages/IncomeDetail'
import GoalDetail from './pages/GoalDetail'
import './App.css'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/expenses" element={<ExpenseList />} />
        <Route path="/income" element={<IncomeList />} />
        <Route path="/budgets" element={<BudgetList />} />
        <Route path="/goals" element={<GoalList />} />
        <Route path="/expenses/:id" element={<ExpenseDetail />} />
        <Route path="/budgets/:id" element={<BudgetDetail />} />
        <Route path="/income/:id" element={<IncomeDetail />} />
        <Route path="/goals/:id" element={<GoalDetail />} />
      </Routes>
    </Layout>
  )
}

export default App
