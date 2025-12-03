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
import Login from './pages/Login'
import ProtectedRoute from './components/ProtectedRoute'
import CreateExpense from './pages/CreateExpense'
import './App.css'
import RedirectIfAuthenticated from './components/RedirectIfAuthenticated'
import CreateIncome from './pages/CreateIncome'
import EditExpense from './pages/EditExpense'
import CreateBudget from './pages/CreateBudget'
import CreateGoal from './pages/CreateGoal'
import DeleteExpense from './pages/DeleteExpense'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<RedirectIfAuthenticated><Login/></RedirectIfAuthenticated>}/>
        <Route path="/create-expense" element={<ProtectedRoute><CreateExpense /></ProtectedRoute>} />
        <Route path="/create-income" element={<ProtectedRoute><CreateIncome /></ProtectedRoute>} />
        <Route path="/create-budget" element={<ProtectedRoute><CreateBudget /></ProtectedRoute>} />
        <Route path="/create-goal" element={<ProtectedRoute><CreateGoal /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/expenses" element={<ProtectedRoute><ExpenseList /></ProtectedRoute>} />
        <Route path="/income" element={<ProtectedRoute><IncomeList /></ProtectedRoute>} />
        <Route path="/budgets" element={<ProtectedRoute><BudgetList /></ProtectedRoute>} />
        <Route path="/goals" element={<ProtectedRoute><GoalList /></ProtectedRoute>} />
        <Route path="/expenses/:id" element={<ProtectedRoute><ExpenseDetail /></ProtectedRoute>} />
        <Route path="/budgets/:id" element={<ProtectedRoute><BudgetDetail /></ProtectedRoute>} />
        <Route path="/income/:id" element={<ProtectedRoute><IncomeDetail /></ProtectedRoute>} />
        <Route path="/goals/:id" element={<ProtectedRoute><GoalDetail /></ProtectedRoute>} />
        <Route path="/edit-expense/:id" element={<ProtectedRoute><EditExpense /></ProtectedRoute>} />
        <Route path="/delete-expense/:id" element={<ProtectedRoute><DeleteExpense /></ProtectedRoute>} />
      </Routes>
    </Layout>
  )
}

export default App
