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

  const token = localStorage.getItem('access_token');

  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
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
  return await apiRequest("/api/dashboard/")
}

async function fetchExpenses() {
  return await apiRequest("/expenses")
}

async function fetchIncomes() {
  return await apiRequest("/income")
}

async function fetchBudgets() {
  return await apiRequest("/budgets")
}

async function fetchGoals() {
  return await apiRequest("/goals")
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


async function loginUser(username, password) {
  // Prepare the data
  const loginData = {
    username: username,
    password: password
  }

  try {

    const response = await fetch(`${API_BASE_URL}/api/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    });

    if (!response.ok) {
      // If password is wrong, response.ok will be false
      throw new Error('Login failed');
    }

    const data = await response.json();

    // Store the tokens so apiRequest can find them later
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);

    return data;
  } catch (error) {
    console.error("Login Error:", error)
    throw error
  }
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refresh_token");

  if (!refreshToken) {
    throw new Error("No refresh token available");
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ refresh: localStorage.getItem("refresh_token") })
    });

  if (!response.ok) {
    throw new Error("Token refresh failed.")
  }

  const data = await response.json()
  localStorage.setItem('access_token', data.access);
  return data.access
} catch (error) {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token")
  throw error;
  }
}

// Export all API functions
export {
  apiRequest,
  API_BASE_URL,
  fetchDashboardData,
  fetchExpenses,
  fetchIncomes,
  fetchBudgets,
  fetchGoals,
  fetchExpense,
  fetchBudget,
  fetchIncome,
  fetchGoal,
  loginUser,
  refreshAccessToken,
}
