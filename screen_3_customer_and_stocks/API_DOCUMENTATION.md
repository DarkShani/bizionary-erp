# Screen 3: Customer Analytics & Stocks - API Documentation

## Overview
Customer Analytics Dashboard with AI-powered CRM insights, loyalty management, and comprehensive customer behavior tracking.

## Base URL
All endpoints are prefixed with: `/api/screen3/`

---

## 🎯 Key Performance Indicators (KPIs)

### Get Dashboard KPIs
**GET** `/api/screen3/customer-analytics/customers/dashboard_kpis/`

Returns current KPIs with percentage changes:
- Total Customers (with change %)
- Retention Rate (with change %)
- Average Lifetime Value (with change %)
- Churn Risk Percentage (with change %)

**Response Example:**
```json
{
  "total_customers": 12450,
  "total_customers_change": "12.00",
  "retention_rate": "88.00",
  "retention_rate_change": "-2.00",
  "avg_lifetime_value": "45000.00",
  "avg_lifetime_value_change": "5.00",
  "churn_risk_percentage": "5.00",
  "churn_risk_change": "-1.00"
}
```

---

## 👥 Customer Management

### List All Customers
**GET** `/api/screen3/customer-analytics/customers/`

### Create New Customer (Quick Entry)
**POST** `/api/screen3/customer-analytics/customers/`

**Request Body:**
```json
{
  "full_name": "Ahmed Khan",
  "email": "ahmed.khan@example.com",
  "phone": "+92-300-1234567"
}
```

### Get Customer Details
**GET** `/api/screen3/customer-analytics/customers/{id}/`

### Update Customer
**PUT/PATCH** `/api/screen3/customer-analytics/customers/{id}/`

### Delete Customer
**DELETE** `/api/screen3/customer-analytics/customers/{id}/`

### Update Customer Tier
**POST** `/api/screen3/customer-analytics/customers/{id}/update_tier/`

**Request Body:**
```json
{
  "tier": "VIP"  // Options: VIP, REGULAR, NEW
}
```

### Get At-Risk Customers
**GET** `/api/screen3/customer-analytics/customers/at_risk_customers/`

Returns customers flagged with high churn risk.

**Response Example:**
```json
{
  "count": 12,
  "customers": [...]
}
```

### Get VIP Customers
**GET** `/api/screen3/customer-analytics/customers/vip_customers/`

**Response Example:**
```json
{
  "count": 45,
  "customers": [...]
}
```

---

## 📊 Loyalty Distribution

### Get Loyalty Tier Distribution
**GET** `/api/screen3/customer-analytics/customers/loyalty_distribution/`

Returns percentage distribution across loyalty tiers.

**Response Example:**
```json
[
  {
    "tier": "VIP Tier",
    "count": 45,
    "percentage": "45.00"
  },
  {
    "tier": "Regulars",
    "count": 32,
    "percentage": "32.00"
  },
  {
    "tier": "New Signups",
    "count": 23,
    "percentage": "23.00"
  }
]
```

---

## 📈 Customer Behavior Analytics

### Get Behavior Frequency Trends
**GET** `/api/screen3/customer-analytics/customers/behavior_frequency/`

Returns monthly purchase frequency trends (last 6 months).

**Response Example:**
```json
[
  {
    "month": "JAN",
    "frequency_index": 345
  },
  {
    "month": "FEB",
    "frequency_index": 289
  },
  ...
]
```

### List Customer Behaviors
**GET** `/api/screen3/customer-analytics/behavior/`

### Get Behavior by Customer
**GET** `/api/screen3/customer-analytics/behavior/by_customer/?customer_id={id}`

---

## 🛍️ Purchase Records

### List All Purchases
**GET** `/api/screen3/customer-analytics/purchases/`

### Create Purchase Record
**POST** `/api/screen3/customer-analytics/purchases/`

**Request Body:**
```json
{
  "customer": 1,
  "purchase_date": "2026-03-04",
  "amount": "15000.00",
  "items_count": 5,
  "payment_method": "Card"
}
```

### Get Purchase Details
**GET** `/api/screen3/customer-analytics/purchases/{id}/`

---

## 🔔 Recent Activities

### Get Recent Activities
**GET** `/api/screen3/customer-analytics/activities/`

Query Parameters:
- `limit` (optional): Number of activities to return (default: 10)

**Response Example:**
```json
[
  {
    "id": 1,
    "customer": 5,
    "customer_name": "Ahmed Khan",
    "activity_type": "SALE",
    "description": "New sale record created",
    "metadata": {},
    "timestamp": "2026-03-04T20:15:30Z",
    "time_ago": "2h ago"
  },
  ...
]
```

---

## 🤖 AI CRM Insights

### Get All Active Insights
**GET** `/api/screen3/customer-analytics/insights/active_insights/`

Returns AI-generated insights and recommendations.

**Response Example:**
```json
[
  {
    "id": 1,
    "insight_type": "SEGMENT",
    "title": "VIP Customers Growing",
    "description": "VIP customer segment shows strong growth with 4.2% increase...",
    "priority": "HIGH",
    "metric_value": "4.2%",
    "recommendation": "Maintain engagement with personalized offers...",
    "action_plan": {
      "steps": [
        "Send personalized thank you emails",
        "Offer exclusive early access to new products"
      ]
    },
    "is_active": true,
    "created_at": "2026-03-04T10:00:00Z"
  },
  {
    "id": 2,
    "insight_type": "CHURN",
    "title": "Churn Alert",
    "description": "12 At-Risk accounts detected in Retail segment...",
    "priority": "CRITICAL",
    "metric_value": "12 accounts",
    "recommendation": "Immediate re-engagement campaign recommended...",
    "action_plan": {
      "actions": [
        "Send win-back email campaign",
        "Offer 20% discount coupon"
      ],
      "at_risk_count": 12,
      "potential_loss": "PKR 540,000"
    }
  }
]
```

### List All Insights
**GET** `/api/screen3/customer-analytics/insights/`

### Create Insight
**POST** `/api/screen3/customer-analytics/insights/`

### Get Insight Details
**GET** `/api/screen3/customer-analytics/insights/{id}/`

---

## 📉 Historical KPIs

### Get KPI History
**GET** `/api/screen3/customer-analytics/kpis/`

### Get KPI Trends
**GET** `/api/screen3/customer-analytics/kpis/trends/?days=30`

Returns KPI trends over specified time period.

---

##  Data Models

### Customer
- `full_name`: String
- `email`: String (unique)
- `phone`: String (optional)
- `loyalty_tier`: Choice (VIP, REGULAR, NEW)
- `is_vip`: Boolean
- `lifetime_value`: Decimal
- `total_purchases`: Integer
- `average_order_value`: Decimal
- `last_purchase_date`: Date
- `registration_date`: Date
- `churn_risk_score`: Integer (0-100)
- `is_at_risk`: Boolean
- `is_active`: Boolean

### CustomerBehavior
- `customer`: ForeignKey
- `month`: String (YYYY-MM)
- `purchase_frequency`: Integer
- `total_spent`: Decimal
- `average_days_between_purchases`: Integer

### CustomerInsight
- `insight_type`: Choice (SEGMENT, UPSELL, CHURN, GROWTH)
- `title`: String
- `description`: Text
- `priority`: Choice (HIGH, MEDIUM, CRITICAL)
- `metric_value`: String
- `recommendation`: Text
- `action_plan`: JSON

---

## 📊 Dashboard Metrics Summary

Based on current data:
- **Total Customers**: 100
- **VIP Tier**: 45%
- **Regulars**: 32%
- **New Signups**: 23%
- **At-Risk Customers**: 13
- **Average Lifetime Value**: PKR 145,605.95
- **Retention Rate**: 94%

---

## 🔧 Testing the APIs

### Using cURL

```bash
# Get Dashboard KPIs
curl http://localhost:8000/api/screen3/customer-analytics/customers/dashboard_kpis/

# Create New Customer
curl -X POST http://localhost:8000/api/screen3/customer-analytics/customers/ \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Test User", "email": "test@example.com"}'

# Get Customer Tier Distribution
curl http://localhost:8000/api/screen3/customer-analytics/customers/loyalty_distribution/

# Get Active Insights
curl http://localhost:8000/api/screen3/customer-analytics/insights/active_insights/
```

---

## 📝 Notes

1. All datetime fields are in ISO 8601 format
2. All monetary values are in PKR (Pakistani Rupees)
3. Pagination is available on list endpoints
4. Authentication may be required (depends on your DRF settings)
5. CORS is configured for development

---

## 🚀 Quick Start

1. **Run migrations** (already done):
   ```bash
   python manage.py migrate
   ```

2. **Insert sample data** (already done):
   ```bash
   python insert_screen3_data.py
   ```

3. **Start the server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the APIs** at:
   - Dashboard KPIs: http://localhost:8000/api/screen3/customer-analytics/customers/dashboard_kpis/
   - API Root: http://localhost:8000/api/screen3/

---

## 📧 Support

For issues or questions, refer to the Django admin panel at http://localhost:8000/admin/
