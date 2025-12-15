// External Libraries
import { Routes, Route } from 'react-router-dom'

// Styles
import './App.css'

// Components
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import RedirectIfAuthenticated from './components/RedirectIfAuthenticated'

// Authentication Pages
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'

// CREATE Pages
import CreateExpense from './pages/CreateExpense'
import CreateIncome from './pages/CreateIncome'
import CreateBudget from './pages/CreateBudget'
import CreateGoal from './pages/CreateGoal'
import CreateProject from './pages/CreateProject'
import CreateClient from './pages/CreateClient'

// READ Pages - Lists
import ExpenseList from './pages/ExpenseList'
import IncomeList from './pages/IncomeList'
import BudgetList from './pages/BudgetList'
import GoalList from './pages/GoalList'
import ProjectList from './pages/ProjectList'
import ClientList from './pages/ClientList'

// READ Pages - Details
import ExpenseDetail from './pages/ExpenseDetail'
import IncomeDetail from './pages/IncomeDetail'
import BudgetDetail from './pages/BudgetDetail'
import GoalDetail from './pages/GoalDetail'
import ProjectDetail from './pages/ProjectDetail'
import ClientDetail from './pages/ClientDetail'

// UPDATE/EDIT Pages
import EditExpense from './pages/EditExpense'
import EditIncome from './pages/EditIncome'
import EditBudget from './pages/EditBudget'
import EditGoal from './pages/EditGoal'
import EditProject from './pages/EditProject'
import EditClient from './pages/EditClient'

// DELETE Pages
import DeleteExpense from './pages/DeleteExpense'
import DeleteIncome from './pages/DeleteIncome'
import DeleteBudget from './pages/DeleteBudget'
import DeleteGoal from './pages/DeleteGoal'
import DeleteProject from './pages/DeleteProject'
import DeleteClient from './pages/DeleteClient'



function App() {
  return (
    <Layout>
      <Routes>
        {/* Authentication */}
        <Route path="/" element={<RedirectIfAuthenticated><Login/></RedirectIfAuthenticated>}/>
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        
        {/* CREATE Routes */}
        <Route path="/create-expense" element={<ProtectedRoute><CreateExpense /></ProtectedRoute>} />
        <Route path="/create-income" element={<ProtectedRoute><CreateIncome /></ProtectedRoute>} />
        <Route path="/create-budget" element={<ProtectedRoute><CreateBudget /></ProtectedRoute>} />
        <Route path="/create-goal" element={<ProtectedRoute><CreateGoal /></ProtectedRoute>} />
        <Route path="/create-project" element={<ProtectedRoute><CreateProject /></ProtectedRoute>} />
        <Route path="/create-client" element={<ProtectedRoute><CreateClient /></ProtectedRoute>} />
        
        {/* READ Routes - Lists */}
        <Route path="/expenses" element={<ProtectedRoute><ExpenseList /></ProtectedRoute>} />
        <Route path="/income" element={<ProtectedRoute><IncomeList /></ProtectedRoute>} />
        <Route path="/budgets" element={<ProtectedRoute><BudgetList /></ProtectedRoute>} />
        <Route path="/goals" element={<ProtectedRoute><GoalList /></ProtectedRoute>} />
        <Route path="/projects" element={<ProtectedRoute><ProjectList /></ProtectedRoute>} />
        <Route path="/clients" element={<ProtectedRoute><ClientList /></ProtectedRoute>} />
        
        {/* READ Routes - Details */}
        <Route path="/expenses/:id" element={<ProtectedRoute><ExpenseDetail /></ProtectedRoute>} />
        <Route path="/income/:id" element={<ProtectedRoute><IncomeDetail /></ProtectedRoute>} />
        <Route path="/budgets/:id" element={<ProtectedRoute><BudgetDetail /></ProtectedRoute>} />
        <Route path="/goals/:id" element={<ProtectedRoute><GoalDetail /></ProtectedRoute>} />
        <Route path="/projects/:id" element={<ProtectedRoute><ProjectDetail /></ProtectedRoute>} />
        <Route path="/clients/:id" element={<ProtectedRoute><ClientDetail /></ProtectedRoute>} />
        
        {/* UPDATE/EDIT Routes */}
        <Route path="/edit-expense/:id" element={<ProtectedRoute><EditExpense /></ProtectedRoute>} />
        <Route path="/edit-income/:id" element={<ProtectedRoute><EditIncome /></ProtectedRoute>} />
        <Route path="/edit-budget/:id" element={<ProtectedRoute><EditBudget /></ProtectedRoute>} />
        <Route path="/edit-goal/:id" element={<ProtectedRoute><EditGoal /></ProtectedRoute>} />
        <Route path="/edit-project/:id" element={<ProtectedRoute><EditProject /></ProtectedRoute>} />
        <Route path="/edit-client/:id" element={<ProtectedRoute><EditClient /></ProtectedRoute>} />
        
        {/* DELETE Routes */}
        <Route path="/delete-expense/:id" element={<ProtectedRoute><DeleteExpense /></ProtectedRoute>} />
        <Route path="/delete-income/:id" element={<ProtectedRoute><DeleteIncome /></ProtectedRoute>} />
        <Route path="/delete-budget/:id" element={<ProtectedRoute><DeleteBudget /></ProtectedRoute>} />
        <Route path="/delete-goal/:id" element={<ProtectedRoute><DeleteGoal /></ProtectedRoute>} />
        <Route path="/delete-project/:id" element={<ProtectedRoute><DeleteProject /></ProtectedRoute>} />
        <Route path="/delete-client/:id" element={<ProtectedRoute><DeleteClient /></ProtectedRoute>} />
      </Routes>
    </Layout>
  )
}

export default App
