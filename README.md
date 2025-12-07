# Expense & Budget Tracker

A full-stack web application for tracking expenses, income, budgets, and financial goals. Built with **React** (frontend) and **Django REST Framework** (backend) with **SQLite database**.

Originally developed as a command-line application for the **HyperionDev Software Engineering Bootcamp Capstone Project**, now evolved into a modern web application.

---

## Features

### Authentication & Security
- JWT-based authentication
- Protected routes for authenticated users only
- User-specific data isolation
- Secure token storage and refresh

### Transaction Management
- **Create** expenses and income with category, date, amount, and notes
- **View** all transactions in organized lists
- **Edit** existing expenses and income
- **Delete** transactions (coming soon)
- Filter by category and date range

### Budget System
- Create budgets for categories with start/end dates
- Track spending percentage and remaining amount
- Automatic calculation of budget progress
- View budgets by category

### Goal Tracking
- Set financial goals with target amounts and deadlines
- Track progress with status indicators (Not Started, In Progress, Completed)
- View goals with remaining amounts and deadlines

### Dashboard
- Overview of total income and expenses
- Recent transactions display
- Quick navigation to detail pages
- Summary statistics

---

## Tech Stack

### Frontend
- **React** - UI framework
- **React Router** - Client-side routing
- **Vite** - Build tool and dev server
- **CSS3** - Styling

### Backend
- **Django** - Web framework
- **Django REST Framework** - API development
- **Django REST Framework Simple JWT** - Authentication
- **SQLite** - Database

---

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Git

### Backend Setup

```bash
# Navigate to project directory
cd AlexHollingsworth_Expense_Tracker_Capstone

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# (Optional) Create superuser
python manage.py createsuperuser

# (Optional) Populate with demo data
python manage.py seed_demo

# Start Django development server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port Vite assigns)

---

## Usage

### Getting Started

1. **Start Backend**: Run `python manage.py runserver` in the project root
2. **Start Frontend**: Run `npm run dev` in the `frontend` directory
3. **Access Application**: Open `http://localhost:5173` in your browser
4. **Login**: Use your superuser credentials or create a new account

### Creating Transactions

- Click **Create** in the navigation bar
- Select **Expense** or **Income**
- Fill in the form (amount, date, category, optional note)
- Submit to save

### Managing Budgets

- Click **Create** → **Budget**
- Select a category
- Enter amount, start date, and end date
- Budget progress is calculated automatically

### Setting Goals

- Click **Create** → **Goal**
- Enter goal name, target amount, deadline, and status
- Track your progress toward financial goals

### Editing Transactions

- Navigate to **Expenses** or **Income** list
- Click on any transaction card
- Click **Edit** button
- Update fields and save

---

## API Endpoints

### Authentication
- `POST /api/token/` - Login (obtain access token)
- `POST /api/token/refresh/` - Refresh access token

### Transactions
- `GET /expenses/` - List all expenses (user-specific)
- `POST /expenses/` - Create new expense
- `GET /expenses/{id}/` - Get expense details
- `PUT /expenses/{id}/` - Update expense
- `GET /income/` - List all income (user-specific)
- `POST /income/` - Create new income

### Budgets & Goals
- `GET /budgets/` - List all budgets (user-specific)
- `POST /budgets/` - Create new budget
- `GET /goals/` - List all goals (user-specific)
- `POST /goals/` - Create new goal

### Categories
- `GET /categories/` - List all categories

### Dashboard
- `GET /api/dashboard/` - Get dashboard summary data

---

## Project Structure

```
AlexHollingsworth_Expense_Tracker_Capstone/
├── et_transactions/          # Django app
│   ├── models.py             # Database models
│   ├── views.py              # API ViewSets
│   ├── serializers.py        # DRF serializers
│   └── management/commands/  # Custom commands
│       └── seed_demo.py      # Demo data seeder
├── expense_tracker/          # Django project settings
│   ├── settings.py           # Django configuration
│   └── urls.py               # URL routing
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── contexts/        # React Context (Auth)
│   │   ├── pages/           # Page components
│   │   └── services/        # API service layer
│   └── package.json
├── db.sqlite3               # SQLite database
└── requirements.txt         # Python dependencies
```

---

## Key Features Implementation

### User Authentication
- JWT tokens stored in localStorage
- Automatic token refresh
- Protected routes redirect unauthenticated users
- Login page redirects authenticated users

### User-Specific Data
- All transactions, budgets, and goals are filtered by authenticated user
- Foreign key relationships ensure data isolation
- Automatic user assignment on creation

### Form Handling
- Client-side form validation
- Success/error message display
- Form reset after successful submission
- Loading states (spinner CSS included)

---

## Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend (if tests are set up)
cd frontend
npm test
```

### Database Migrations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend (use production WSGI server)
# Configure production settings in settings.py
```

---

## Design Decisions

### Backend
- **Django REST Framework**: Provides automatic CRUD endpoints via ModelViewSet
- **JWT Authentication**: Stateless authentication suitable for SPA
- **User Foreign Keys**: All models linked to User for multi-user support
- **Serializer Pattern**: Read-only category objects, write-only category_id for clean API

### Frontend
- **React Context**: Global authentication state management
- **Protected Routes**: Route-level authentication guards
- **API Service Layer**: Centralized API calls with error handling
- **Component-Based**: Reusable form components for Create/Edit operations

---

## Known Limitations & Future Enhancements

### Current Limitations
- Delete functionality not yet implemented
- No pagination for large lists
- No advanced filtering/search
- No data export functionality  
- No data visualization/charts

### Planned Enhancements
- Loading spinners during API calls
- Form validation improvements
- Date range filtering
- Category management UI
- Data visualization (charts)
- Export to CSV/PDF
- Pagination for lists

---

## Author
Alex Hollingsworth  
HyperionDev Software Engineering Bootcamp  
Capstone Project - 2024

---

## License
This project was created as part of a coding bootcamp capstone project.
