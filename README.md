# Expense & Budget Tracker

A full-stack web application designed for freelance and independent musicians to track their expenses, income, budgets, financial goals, projects, and clients. Built with **React** (frontend) and **Django REST Framework** (backend) with **SQLite** (development) and **PostgreSQL** (production) support.

Originally developed as a command-line application for the **HyperionDev Software Engineering Bootcamp Capstone Project**, now evolved into a modern web application tailored for music professionals.

---

## Features

### Authentication & Security
- JWT-based authentication with automatic token refresh
- Protected routes for authenticated users only
- User-specific data isolation
- Secure token storage in localStorage
- Session expiration handling

### Transaction Management
- **Create, Read, Update, Delete** expenses and income
- Category-based organization
- Date tracking and optional notes
- Filter by category and date range
- User-specific transaction lists

### Budget System
- **Full CRUD operations**: Create, Read, Update, and Delete budgets
- Create budgets for categories with start/end dates
- Track spending percentage and remaining amount
- Automatic calculation of budget progress
- View budgets by category
- Edit existing budgets
- Delete budgets when no longer needed

### Goal Tracking
- **Full CRUD operations**: Create, Read, Update, and Delete goals
- Set financial goals with target amounts and deadlines
- Track progress with status indicators (Not Started, In Progress, Completed)
- View goals with remaining amounts and deadlines
- Edit goals to update targets, deadlines, or status
- Delete goals when completed or no longer relevant

### Project & Client Management
- Create and manage projects
- Associate expenses and income with projects
- Create and manage clients
- Link transactions to clients for better organization

### Dashboard
- Overview of total income and expenses
- Net total calculation
- Recent transactions display
- Quick navigation to detail pages
- Summary statistics for budgets and goals

---

## Tech Stack

### Frontend
- **React 19** - UI framework
- **React Router 7** - Client-side routing
- **Vite 7** - Build tool and dev server
- **CSS3** - Styling (organized in `src/styles/`)

### Backend
- **Django 5.2.8** - Web framework
- **Django REST Framework 3.16** - API development
- **Django REST Framework Simple JWT** - Authentication
- **SQLite** - Development database
- **PostgreSQL** - Production database (via psycopg2)
- **Gunicorn** - Production WSGI server
- **django-phonenumber-field** - Phone number validation

---

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Git
- PostgreSQL (for production deployment)

### Backend Setup

```bash
# Navigate to project directory
cd AlexHollingsworth_Expense_Tracker_Capstone

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment variables template
cp .env.example .env
# Edit .env and set your SECRET_KEY and other variables

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

# Copy environment variables template
cp .env.example .env
# Edit .env if you need to change the API URL (default: http://localhost:8000)

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Environment Variables

### Backend (.env)
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False for production
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your domain for production
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# PostgreSQL (optional - leave commented for SQLite development)
# DB_NAME=expense_tracker_db
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Frontend (.env)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

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
- Fill in the form (amount, date, category, optional note, project, client)
- Submit to save

### Managing Budgets

- **Create**: Click **Create** → **Budget**
  - Select a category
  - Enter amount, start date, and end date
  - Budget progress is calculated automatically
- **View**: Navigate to **Budgets** to see all your budgets
- **Edit**: Click on any budget to view details, then click **Edit**
- **Delete**: Click on any budget, then click **Delete** to remove it

### Setting Goals

- **Create**: Click **Create** → **Goal**
  - Enter goal name, target amount, deadline, and status
  - Track your progress toward financial goals
- **View**: Navigate to **Goals** to see all your goals
- **Edit**: Click on any goal to view details, then click **Edit** to update
- **Delete**: Click on any goal, then click **Delete** to remove it

### Managing Projects & Clients

- Click **Create** → **Project** or **Client**
- Fill in the details
- Associate transactions with projects/clients for better organization

### Editing & Deleting

- Navigate to any list (Expenses, Income, Budgets, Goals, Projects, Clients)
- Click on any item to view details
- Use **Edit** to update or **Delete** to remove

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
- `DELETE /expenses/{id}/` - Delete expense
- `GET /income/` - List all income (user-specific)
- `POST /income/` - Create new income
- `GET /income/{id}/` - Get income details
- `PUT /income/{id}/` - Update income
- `DELETE /income/{id}/` - Delete income

### Budgets & Goals
- `GET /budgets/` - List all budgets (user-specific)
- `POST /budgets/` - Create new budget
- `GET /budgets/{id}/` - Get budget details
- `PUT /budgets/{id}/` - Update budget
- `DELETE /budgets/{id}/` - Delete budget
- `GET /goals/` - List all goals (user-specific)
- `POST /goals/` - Create new goal
- `GET /goals/{id}/` - Get goal details
- `PUT /goals/{id}/` - Update goal
- `DELETE /goals/{id}/` - Delete goal

### Projects & Clients
- `GET /projects/` - List all projects (user-specific)
- `POST /projects/` - Create new project
- `GET /projects/{id}/` - Get project details
- `PUT /projects/{id}/` - Update project
- `DELETE /projects/{id}/` - Delete project
- `GET /clients/` - List all clients (user-specific)
- `POST /clients/` - Create new client
- `GET /clients/{id}/` - Get client details
- `PUT /clients/{id}/` - Update client
- `DELETE /clients/{id}/` - Delete client

### Categories
- `GET /categories/` - List all categories
- `GET /categories/?type=EXPENSE` - Filter by type
- `GET /categories/?type=INCOME` - Filter by type

### Dashboard
- `GET /api/dashboard/` - Get dashboard summary data

---

## Project Structure

```
AlexHollingsworth_Expense_Tracker_Capstone/
├── api/                      # Django app (API backend)
│   ├── models.py             # Database models
│   ├── views.py              # API ViewSets
│   ├── serializers.py        # DRF serializers
│   ├── admin.py              # Django admin configuration
│   ├── data/                 # Data files
│   │   └── categories.py     # Default categories
│   ├── management/commands/  # Custom commands
│   │   └── seed_demo.py      # Demo data seeder
│   ├── migrations/           # Database migrations
│   └── tests/                # Test files
├── expense_tracker/          # Django project settings
│   ├── settings.py           # Django configuration
│   └── urls.py               # URL routing
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   │   ├── Layout.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── FilterBar.jsx
│   │   ├── contexts/         # React Context
│   │   │   └── AuthContext.jsx
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── ExpenseList.jsx
│   │   │   └── ... (all CRUD pages)
│   │   ├── services/         # API service layer
│   │   │   └── api.js
│   │   └── styles/           # CSS files
│   │       ├── App.css
│   │       ├── Dashboard.css
│   │       └── ...
│   └── package.json
├── .env.example              # Environment variables template
├── .gitignore
├── db.sqlite3                # SQLite database (development)
├── manage.py
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Key Features Implementation

### User Authentication
- JWT tokens stored in localStorage
- Automatic token refresh on 401 errors
- Protected routes redirect unauthenticated users to login
- Login page redirects authenticated users to dashboard
- Session expiration handling with user-friendly messages

### User-Specific Data
- All transactions, budgets, goals, projects, and clients are filtered by authenticated user
- Foreign key relationships ensure data isolation
- Automatic user assignment on creation

### Form Handling
- Client-side form validation
- Success/error message display
- Form reset after successful submission
- Loading states during API calls

### Error Handling
- Centralized API error handling
- Automatic token refresh on expiration
- User-friendly error messages
- Network error handling

---

## Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Run specific test files
python manage.py test api.test_views
python manage.py test api.test_validation
python manage.py test api.test_auth
```

### Database Migrations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend - collect static files
python manage.py collectstatic

# Backend - use production WSGI server
gunicorn expense_tracker.wsgi:application
```

---

## Production Deployment

### Environment Setup
1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up PostgreSQL database
5. Configure `CORS_ALLOWED_ORIGINS` with your frontend URL
6. Set up static file serving (nginx, etc.)

### Database
- Development: SQLite (automatic when `DB_NAME` is not set)
- Production: PostgreSQL (set `DB_NAME`, `DB_USER`, `DB_PASSWORD` in `.env`)

### Static Files
- Run `python manage.py collectstatic` before deployment
- Static files will be collected in `staticfiles/` directory
- Serve via nginx or your web server

---

## Design Decisions

### Backend
- **Django REST Framework**: Provides automatic CRUD endpoints via ModelViewSet
- **JWT Authentication**: Stateless authentication suitable for SPA
- **User Foreign Keys**: All models linked to User for multi-user support
- **Serializer Pattern**: Read-only category objects, write-only category_id for clean API
- **Environment-based Configuration**: Automatic SQLite/PostgreSQL switching

### Frontend
- **React Context**: Global authentication state management
- **Protected Routes**: Route-level authentication guards
- **API Service Layer**: Centralized API calls with error handling and token refresh
- **Component-Based**: Reusable form components for Create/Edit operations
- **Organized Styles**: CSS files in dedicated `styles/` directory

---

## Future Enhancements

- Advanced filtering and search
- Data export (CSV/PDF)
- Data visualization (charts and graphs)
- Pagination for large lists
- Date range filtering UI
- Category management UI
- Recurring transactions
- Budget alerts and notifications
- Multi-currency support

---

## Author
Alex Hollingsworth  

---

## License
This project was created as part of a coding bootcamp capstone project.

---

## Evolution & Use Case

What started as a capstone project has evolved into a full production-ready tool designed specifically for musicians to track their income and expenses. The application provides a comprehensive solution for managing financial data related to:

- **Performance Income**: Track earnings from gigs, concerts, and live performances
- **Recording Revenue**: Monitor income from recording sessions, studio work, and production projects
- **Teaching Income**: Record earnings from music lessons and workshops
- **Project-Based Tracking**: Organize income and expenses by specific projects or albums
- **Client Management**: Keep track of venues, promoters, and collaborators
- **Budget Planning**: Set budgets for tours, recording sessions, and equipment purchases
- **Financial Goals**: Set and track savings goals for equipment, studio time, or career milestones

The application's user-friendly interface and robust API make it an ideal tool for independent musicians, bands, and music professionals who need to manage their finances without the complexity of traditional accounting software.
