const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

let isRefreshing = false
let refreshPromise = null

async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`

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

    if (response.status === 401) {
      // Skip refresh for login/token endpoints to avoid infinite loops
      if (endpoint.includes('/api/token/')) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`)
      }

      // Try to refresh token and retry request
      try {
        await refreshTokenIfNeeded()

        // Retry the original request with new token
        const newToken = localStorage.getItem('access_token')
        if (newToken) {
          config.headers['Authorization'] = `Bearer ${newToken}`
          const retryResponse = await fetch(url, config)

          if (!retryResponse.ok) {
            throw new Error(`API Error: ${retryResponse.status} ${retryResponse.statusText}`)
          }

          // Handle empty responses
          if (retryResponse.status === 204 || retryResponse.headers.get('content-length') === '0') {
            return null
          }

          return await retryResponse.json()
        }
      } catch (refreshError) {
        // Refresh failed - clear tokens and redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        // Redirect to login page
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }

        throw new Error('Session expired. Please login again.')
      }
    }

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }

    // Handle empty responses (e.g., 204 No Content for DELETE requests)
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return null
    }

    // Parse and return JSON response
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API Request failed:', error)
    throw error
  }

}

// Helper function to refresh token (handles concurrent requests)
async function refreshTokenIfNeeded() {
  // If already refreshing, wait for that promise
  if (isRefreshing && refreshPromise) {
    return refreshPromise
  }

  // Start refresh process
  isRefreshing = true
  refreshPromise = refreshAccessToken()
    .finally(() => {
      isRefreshing = false
      refreshPromise = null
    })

  return refreshPromise
}

async function fetchDashboardData() {
  return await apiRequest("/api/dashboard/")
}

async function fetchExpenses() {
  return await apiRequest("/expenses/")
}

async function fetchIncomes() {
  return await apiRequest("/income/")
}

async function fetchBudgets() {
  return await apiRequest("/budgets/")
}

async function fetchGoals() {
  return await apiRequest("/goals/")
}

async function fetchProjects() {
  return await apiRequest("/projects/")
}

async function fetchClients() {
  return await apiRequest("/clients/")
}

async function fetchCategories(type = null) {
  const endpoint = type ? `/categories/?type=${type}` : "/categories/";
  return await apiRequest(endpoint);
}

async function fetchExpense(id) {
  return await apiRequest(`/expenses/${id}`)
}

async function fetchIncome(id) {
  return await apiRequest(`/income/${id}`)
}

async function fetchBudget(id) {
  return await apiRequest(`/budgets/${id}`)
}

async function fetchGoal(id) {
  return await apiRequest(`/goals/${id}`)
}

async function fetchProject(id) {
  return await apiRequest(`/projects/${id}`)
}

async function fetchClient(id) {
  return await apiRequest(`/clients/${id}`)
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

async function createCategory(categoryData) {
  const createdCategory = await apiRequest("/categories/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(categoryData)
  });
  return createdCategory;
}

async function createExpense(expenseData) {
  const createdExpense = await apiRequest("/expenses/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(expenseData)
  });
  return createdExpense;
}

async function createIncome(incomeData) {
  const createdIncome = await apiRequest("/income/", {
    method: 'POST',
    body: JSON.stringify(incomeData)
  });
  return createdIncome;
}

async function updateExpense(id, expenseData) {
  const updatedExpense = await apiRequest(`/expenses/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(expenseData)
  });
  return updatedExpense;
}

async function updateIncome(id, incomeData) {
  const updatedIncome = await apiRequest(`/income/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(incomeData)
  });
  return updatedIncome;
}

async function updateBudget(id, budgetData) {
  const updatedBudget = await apiRequest(`/budgets/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(budgetData)
  });
  return updatedBudget;
}

async function updateGoal(id, goalData) {
  const updatedGoal = await apiRequest(`/goals/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(goalData)
  });
  return updatedGoal;
}

async function updateProject(id, projectData) {
  const updatedProject = await apiRequest(`/projects/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(projectData)
  });
  return updatedProject;
}

async function updateClient(id, clientData) {
  const updatedClient = await apiRequest(`/clients/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(clientData)
  });
  return updatedClient;
}

async function createBudget(budgetData) {
  const createdBudget = await apiRequest("/budgets/", {
    method: 'POST',
    body: JSON.stringify(budgetData)
  });
  return createdBudget;
}

async function createGoal(goalData) {
  const createdGoal = await apiRequest("/goals/", {
    method: 'POST',
    body: JSON.stringify(goalData)
  });
  return createdGoal;
}

async function deleteExpense(id) {
  await apiRequest(`/expenses/${id}/`, {
    method: 'DELETE'
  });
  // DELETE requests typically return 204 No Content, so no data to return
}

async function deleteIncome(id) {
  await apiRequest(`/income/${id}/`, {
    method: 'DELETE'
  });
}

async function deleteBudget(id) {
  await apiRequest(`/budgets/${id}/`, {
    method: 'DELETE'
  });
}

async function deleteGoal(id) {
  await apiRequest(`/goals/${id}/`, {
    method: 'DELETE'
  });
}

async function deleteProject(id) {
  await apiRequest(`/projects/${id}/`, {
    method: 'DELETE'
  });
}

async function deleteClient(id) {
  await apiRequest(`/clients/${id}/`, {
    method: 'DELETE'
  });
}

async function createProject(projectData) {
  const createdProject = await apiRequest("/projects/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(projectData)
  });
  return createdProject;
}

async function createClient(clientData) {
  const createdClient = await apiRequest("/clients/", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(clientData)
  });
  return createdClient;
}

export {
  apiRequest,
  API_BASE_URL,
  fetchDashboardData,
  fetchExpenses,
  fetchIncomes,
  fetchBudgets,
  fetchGoals,
  fetchProjects,
  fetchClients,
  fetchExpense,
  fetchBudget,
  fetchIncome,
  fetchGoal,
  fetchProject,
  fetchClient,
  loginUser,
  refreshAccessToken,
  fetchCategories,
  createExpense,
  createIncome,
  updateExpense,
  updateIncome,
  updateBudget,
  updateGoal,
  updateProject,
  updateClient,
  createBudget,
  createProject,
  createClient,
  createGoal,
  deleteExpense,
  deleteIncome,
  deleteBudget,
  deleteGoal,
  deleteProject,
  deleteClient,
  createCategory,
}
