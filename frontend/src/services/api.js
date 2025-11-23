/**
 * API Service Layer
 * 
 * This file contains functions to communicate with the Django backend API.
 * All API calls should go through functions defined here.
 */

// Base URL for the Django backend
// In development, Django typically runs on http://localhost:8000
// TODO: When we create API endpoints, they'll be at /api/ or /transactions/api/
const API_BASE_URL = 'http://localhost:8000'

/**
 * Helper function to make API requests
 * This is a reusable wrapper around fetch() for consistency
 * 
 * @param {string} endpoint - The API endpoint (e.g., '/transactions/api/expenses')
 * @param {object} options - Fetch options (method, headers, body, etc.)
 * @returns {Promise} - The parsed JSON response
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  
  // Set default headers
  const defaultHeaders = {
    'Content-Type': 'application/json',
  }
  
  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  }
  
  try {
    const response = await fetch(url, config)
    
    // Check if response is ok (status 200-299)
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }
    
    // Parse and return JSON response
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API Request failed:', error)
    throw error
  }
}

/**
 * Fetch dashboard data
 * This will eventually call: GET /transactions/api/dashboard/
 * For now, returns mock data until we create the Django API endpoint
 * 
 * @returns {Promise<Object>} Dashboard data with expenses, income, budgets, goals, and totals
 */
async function fetchDashboardData() {
  // TODO: Replace with real API call once Django endpoint is created
  // return await apiRequest('/transactions/api/dashboard/')
  
  // Mock data that matches what Django DashboardView returns
  // This lets us build the UI before the API exists
  return {
    recent_expenses: [
      { id: 1, amount: '45.50', date: '2024-12-20', category: { name: 'Groceries' }, note: 'Weekly shopping' },
      { id: 2, amount: '25.00', date: '2024-12-19', category: { name: 'Gas' }, note: 'Fuel' },
      { id: 3, amount: '12.99', date: '2024-12-18', category: { name: 'Entertainment' }, note: 'Netflix' },
    ],
    recent_income: [
      { id: 1, amount: '3500.00', date: '2024-12-01', category: { name: 'Salary' }, note: 'Monthly salary' },
      { id: 2, amount: '500.00', date: '2024-12-15', category: { name: 'Freelance' }, note: 'Website project' },
      { id: 3, amount: '1000.00', date: '2024-12-10', category: { name: 'Investments' }, note: 'Stock market' },
    ],
    recent_budgets: [
      { id: 1, amount: '400.00', category: { name: 'Groceries' }, start_date: '2024-12-01', end_date: '2024-12-31' },
      { id: 2, amount: '100.00', category: { name: 'Entertainment' }, start_date: '2024-12-01', end_date: '2024-12-31' },
      { id: 3, amount: '1000.00', category: { name: 'Car' }, start_date: '2024-12-01', end_date: '2024-12-31' },
    ],
    recent_goals: [
      { id: 1, name: 'Emergency Fund', target: '5000.00', deadline: '2025-06-01', status: 'On Track' },
      { id: 2, name: 'Vacation', target: '2000.00', deadline: '2025-08-01', status: 'Not Started' },
      { id: 3, name: 'Car', target: '10000.00', deadline: '2026-01-01', status: 'On Track' },
    ],
    expense_total: 1250.50,
    income_total: 4000.00,
    net_total: 2749.50,
    number_of_budgets: 2,
    number_of_goals: 3,
  }
}

async function fetchExpenses() {
  // TODO: Replace with real API call once Django endpoint is created
  // return await apiRequest('/transactions/api/expenses/')
  
  // Mock data for now
  return [
    { id: 1, amount: '45.50', date: '2024-12-20', category: { name: 'Groceries' }, note: 'Weekly shopping' },
    { id: 2, amount: '25.00', date: '2024-12-19', category: { name: 'Gas' }, note: 'Fuel' },
    { id: 3, amount: '12.99', date: '2024-12-18', category: { name: 'Entertainment' }, note: 'Netflix' },
    { id: 4, amount: '150.00', date: '2024-12-17', category: { name: 'Utilities' }, note: 'Electric bill' },
    { id: 5, amount: '35.75', date: '2024-12-16', category: { name: 'Dining' }, note: 'Restaurant dinner' },
  ]
}

async function fetchIncomes() {
  return [
    { id: 1, amount: '3500.00', date: '2024-12-01', category: { name: 'Salary' }, note: 'Monthly salary' },
    { id: 2, amount: '500.00', date: '2024-12-15', category: { name: 'Freelance' }, note: 'Website project' },
    { id: 3, amount: '1000.00', date: '2024-12-10', category: { name: 'Investments' }, note: 'Stock market' },
    { id: 4, amount: '200.00', date: '2024-12-05', category: { name: 'Side Hustle' }, note: 'Tutoring' },
    { id: 5, amount: '1500.00', date: '2024-12-01', category: { name: 'Bonus' }, note: 'Year-end bonus' },
  ]
}

async function fetchBudgets() {
  return [
    { id: 1, amount: '400.00', category: { name: 'Groceries' }, start_date: '2024-12-01', end_date: '2024-12-31' },
    { id: 2, amount: '100.00', category: { name: 'Entertainment' }, start_date: '2024-12-01', end_date: '2024-12-31' },
    { id: 3, amount: '1000.00', category: { name: 'Car' }, start_date: '2024-12-01', end_date: '2024-12-31' },
  ]
}

async function fetchGoals() {
  return [
    { id: 1, name: 'Emergency Fund', target: '5000.00', deadline: '2025-06-01', status: 'On Track' },
    { id: 2, name: 'Vacation', target: '2000.00', deadline: '2025-08-01', status: 'Not Started' },
    { id: 3, name: 'Car', target: '10000.00', deadline: '2026-01-01', status: 'On Track' },
  ]
}

async function fetchExpense(id) {
    // Get all expenses and find the one with matching ID
    const expenses = await fetchExpenses()
    return expenses.find(expense => expense.id === parseInt(id))
}

async function fetchBudget(id) {
    // Get all budgets and find the one with matching ID
    const budgets = await fetchBudgets()
    return budgets.find(budget => budget.id === parseInt(id))
}

async function fetchIncome(id) {
    // Get all income and find the one with matching ID
    const incomes = await fetchIncomes()
    return incomes.find(income => income.id === parseInt(id))
}

async function fetchGoal(id) {
    // Get all goals and find the one with matching ID
    const goals = await fetchGoals()
    return goals.find(goal => goal.id === parseInt(id))
}


// Export all API functions
export { apiRequest, API_BASE_URL, fetchDashboardData, fetchExpenses, fetchIncomes, fetchBudgets, fetchGoals, fetchExpense, fetchBudget, fetchIncome, fetchGoal }

