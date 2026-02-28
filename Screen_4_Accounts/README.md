# Screen 4: Accounts & Finance Module

## 📋 Overview

A **completely independent** Django REST API module for managing financial data in your ERP system. This app handles revenue tracking, expense management, invoicing, and financial analytics.

---

## 🏗️ Architecture

```
Frontend (React/Vue) 
    ↓
    HTTP Request
    ↓
Django REST View (views.py)
    ↓
Service Layer (services.py) - Business Logic
    ↓
Django ORM (models.py)
    ↓
MySQL Database
    ↓
JSON Response → Frontend
```

---

## 📁 Project Structure

```
accounts/
├── __init__.py
├── admin.py              # Django admin configuration
├── apps.py               # App configuration
├── models.py             # Database models (Revenue, Expense, Invoice)
├── serializers.py        # DRF serializers for API responses
├── services.py           # Business logic layer
├── views.py              # API endpoints
├── urls.py               # URL routing
└── migrations/           # Database migrations
```

---

## 📊 Database Models

### 1. Revenue Model
Tracks all income sources for the business.

**Fields:**
- `id` (Auto) - Primary key
- `source` (CharField) - Revenue source name
- `amount` (DecimalField) - Revenue amount
- `date` (DateField) - Date of revenue
- `description` (TextField) - Optional description
- `created_at` (DateTimeField) - Record creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Table:** `screen4_revenue`

### 2. Expense Model
Tracks all business expenses by category.

**Fields:**
- `id` (Auto) - Primary key
- `category` (CharField) - Expense category (PAYROLL, MARKETING, etc.)
- `amount` (DecimalField) - Expense amount
- `date` (DateField) - Date of expense
- `vendor` (CharField) - Vendor/supplier name
- `description` (TextField) - Optional description
- `created_at` (DateTimeField) - Record creation timestamp
- `updated_at` (DateTimeField) - Last update timestamp

**Table:** `screen4_expense`

**Expense Categories:**
- PAYROLL
- MARKETING
- RENT_UTILITIES
- SUPPLIES
- TECHNOLOGY
- TRAVEL
- OTHER

### 3. Invoice Model
Tracks invoices issued to clients.

**Fields:**
- `id` (Auto) - Primary key
- `invoice_number` (CharField, Unique) - Invoice identifier
- `client_name` (CharField) - Client name
- `amount` (DecimalField) - Invoice amount
- `status` (CharField) - Payment status
- `due_date` (DateField) - Payment due date
- `description` (TextField) - Optional description
- `created_at` (DateTimeField) - Invoice creation date
- `updated_at` (DateTimeField) - Last update timestamp

**Table:** `screen4_invoice`

**Invoice Statuses:**
- PAID
- PENDING
- OVERDUE
- CANCELLED

---

## 🔌 API Endpoints

### Dashboard KPIs

#### GET `/api/accounts/kpis/`
Returns all key performance indicators.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_revenue": 2675000.00,
    "total_expense": 1217100.00,
    "net_profit": 1457900.00,
    "cash_flow": 1457900.00
  }
}
```

---

### Analytics Endpoints

#### GET `/api/accounts/trend/`
Returns monthly income vs expense trend.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "month": "2025-08",
      "income": 303000.00,
      "expense": 183500.00
    },
    {
      "month": "2025-09",
      "income": 457000.00,
      "expense": 198000.00
    }
  ]
}
```

#### GET `/api/accounts/recent-invoices/`
Returns the 5 most recent invoices.

**Query Parameters:**
- `limit` (optional, default: 5) - Number of invoices to return

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "invoice_number": "INV-0082",
      "client_name": "TechNow Solutions",
      "amount": "45000.00",
      "status": "PAID",
      "status_display": "Paid",
      "due_date": "2024-10-28",
      "description": "Software development services",
      "created_at": "2024-10-01T00:00:00Z",
      "updated_at": "2024-10-01T00:00:00Z"
    }
  ]
}
```

#### GET `/api/accounts/expense-categories/`
Returns expense breakdown by category with percentages.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "category": "PAYROLL",
      "total": 625000.00,
      "count": 7,
      "percentage": 55.32
    },
    {
      "category": "MARKETING",
      "total": 284000.00,
      "count": 7,
      "percentage": 25.12
    }
  ]
}
```

---

### CRUD Endpoints

#### Revenue Management

- `GET /api/accounts/revenues/` - List all revenues
- `POST /api/accounts/revenues/` - Create new revenue
- `GET /api/accounts/revenues/<id>/` - Get specific revenue
- `PUT /api/accounts/revenues/<id>/` - Update revenue
- `DELETE /api/accounts/revenues/<id>/` - Delete revenue

**Example POST Request:**
```json
{
  "source": "Product Sales",
  "amount": 50000.00,
  "date": "2026-02-28",
  "description": "Q1 product sales"
}
```

#### Expense Management

- `GET /api/accounts/expenses/` - List all expenses
- `POST /api/accounts/expenses/` - Create new expense
- `GET /api/accounts/expenses/<id>/` - Get specific expense
- `PUT /api/accounts/expenses/<id>/` - Update expense
- `DELETE /api/accounts/expenses/<id>/` - Delete expense

**Example POST Request:**
```json
{
  "category": "MARKETING",
  "amount": 15000.00,
  "date": "2026-02-28",
  "vendor": "Digital Agency",
  "description": "Facebook ads campaign"
}
```

#### Invoice Management

- `GET /api/accounts/invoices/` - List all invoices
- `POST /api/accounts/invoices/` - Create new invoice
- `GET /api/accounts/invoices/<id>/` - Get specific invoice
- `PUT /api/accounts/invoices/<id>/` - Update invoice
- `DELETE /api/accounts/invoices/<id>/` - Delete invoice

**Example POST Request:**
```json
{
  "invoice_number": "INV-0093",
  "client_name": "ABC Corporation",
  "amount": 85000.00,
  "status": "PENDING",
  "due_date": "2026-03-31",
  "description": "Consulting services Q1 2026"
}
```

---

## 🚀 Installation & Setup

### 1. Database Migration

```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

### 2. Insert Sample Data

```bash
python insert_screen4_data.py
```

This will insert:
- 31 revenue records (6 months of data)
- 39 expense records (6 months of data)
- 13 invoice records

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Access Django admin at: `http://localhost:8000/admin/`

---

## 🔧 Service Layer Methods

Located in `services.py`:

### `AccountsService` Class

| Method | Description | Returns |
|--------|-------------|---------|
| `total_revenue()` | Calculate total revenue | Decimal |
| `total_expense()` | Calculate total expenses | Decimal |
| `net_profit()` | Calculate net profit (revenue - expense) | Decimal |
| `cash_flow()` | Calculate cash flow | Decimal |
| `income_vs_expense_trend()` | Monthly income vs expense trend | List[Dict] |
| `recent_invoices(limit=5)` | Get recent invoices | QuerySet |
| `expense_categories_breakdown()` | Expense breakdown by category | List[Dict] |
| `kpi_summary()` | Get all KPIs in one call | Dict |

---

## 📦 Data Flow Example

### Frontend Request:
```javascript
fetch('/api/accounts/kpis/')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Backend Processing:
1. **View** (`views.py`) receives the request
2. **Service** (`services.py`) calculates KPIs using:
   - Django ORM aggregations (Sum, Count)
   - Database-level calculations
3. **Serializer** (`serializers.py`) formats the data
4. **View** returns JSON response

### Response:
```json
{
  "success": true,
  "data": {
    "total_revenue": 2675000.00,
    "total_expense": 1217100.00,
    "net_profit": 1457900.00,
    "cash_flow": 1457900.00
  }
}
```

---

## ✅ Key Features

### ✓ Independent Architecture
- No foreign keys to other apps
- Self-contained data models
- Can be used standalone

### ✓ Production-Ready
- Input validation in serializers
- Error handling in views
- Database indexes for performance
- Proper model meta options

### ✓ Service Layer Pattern
- Business logic separated from views
- Reusable calculation methods
- Easy to test and maintain

### ✓ RESTful APIs
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Consistent JSON response format
- Proper status codes

### ✓ Scalability
- Optimized database queries
- Bulk operations support
- Ready for caching (Redis)
- Prepared for role-based permissions

---

## 🎯 Financial Summary (Sample Data)

Based on the inserted sample data:

```
Total Revenue:  Rs. 2,675,000.00
Total Expense:  Rs. 1,217,100.00
Net Profit:     Rs. 1,457,900.00
```

**Revenue Breakdown:** 31 transactions across 6 months
**Expense Breakdown:** 39 transactions across 6 months
**Invoices:** 13 invoices (various statuses)

---

## 🧪 Testing the APIs

### Using cURL:

```bash
# Get KPIs
curl http://localhost:8000/api/accounts/kpis/

# Get trend data
curl http://localhost:8000/api/accounts/trend/

# Get recent invoices
curl http://localhost:8000/api/accounts/recent-invoices/

# Create new revenue
curl -X POST http://localhost:8000/api/accounts/revenues/ \
  -H "Content-Type: application/json" \
  -d '{"source":"Product Sales","amount":50000,"date":"2026-02-28"}'
```

### Using Python requests:

```python
import requests

# Get KPIs
response = requests.get('http://localhost:8000/api/accounts/kpis/')
print(response.json())

# Create expense
expense_data = {
    "category": "MARKETING",
    "amount": 15000,
    "date": "2026-02-28",
    "vendor": "Ad Agency"
}
response = requests.post(
    'http://localhost:8000/api/accounts/expenses/',
    json=expense_data
)
print(response.json())
```

---

## 🔐 Future Enhancements

### Ready for:
- ✅ Redis caching for KPIs
- ✅ Role-based permissions (Django permissions)
- ✅ Pagination for large datasets
- ✅ Filtering and search functionality
- ✅ Export to PDF/Excel
- ✅ Email notifications for overdue invoices
- ✅ Multi-currency support
- ✅ Budget tracking and alerts

---

## 📝 Notes

1. **Independence**: This app has NO dependencies on products, sales, customers, or any other app.
2. **Data Integrity**: All models include timestamps (created_at, updated_at).
3. **Validation**: Serializers include amount validation (must be > 0).
4. **Indexing**: Database indexes added for date, category, and status fields.
5. **Admin Panel**: Full Django admin integration with custom filters and search.

---

## 🆘 Troubleshooting

### Issue: Migrations not applying
```bash
python manage.py migrate accounts --fake-initial
```

### Issue: Data not showing in admin
Make sure you've registered models in `admin.py` (already done).

### Issue: 404 on API endpoints
Check that `accounts.urls` is included in main `urls.py`:
```python
path('api/accounts/', include('accounts.urls', namespace='accounts')),
```

---

## 📞 Support

For issues or questions:
1. Check Django logs
2. Verify database migrations: `python manage.py showmigrations`
3. Test with Django shell: `python manage.py shell`

---

## 📄 License

Part of the ERP System - Screen 4: Accounts & Finance Module

---

**Created:** February 2026  
**Django Version:** 4.x  
**Database:** MySQL  
**REST Framework:** Django REST Framework
