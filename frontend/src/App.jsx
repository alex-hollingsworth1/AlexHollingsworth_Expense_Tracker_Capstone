import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ExpenseList from './pages/ExpenseList'
import IncomeList from './pages/IncomeList'
import BudgetList from './pages/BudgetList'
import GoalList from './pages/GoalList'
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
      </Routes>
    </Layout>
  )
}

export default App
