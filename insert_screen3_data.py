"""
Data insertion script for Screen 3: Customer Analytics and Stocks
Populates the database with sample customer data, behavior, insights, and KPIs
"""

import os
import django
import random
from datetime import datetime, timedelta, date
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from screen_3_customer_and_stocks.customer_analytics.models import (
    Customer, CustomerBehavior, PurchaseRecord, RecentActivity, 
    CustomerInsight, CustomerKPI
)


def clear_existing_data():
    """Clear existing data from screen 3 tables"""
    print("Clearing existing data...")
    CustomerKPI.objects.all().delete()
    CustomerInsight.objects.all().delete()
    RecentActivity.objects.all().delete()
    PurchaseRecord.objects.all().delete()
    CustomerBehavior.objects.all().delete()
    Customer.objects.all().delete()
    print("✓ Existing data cleared")


def create_customers():
    """Create sample customers"""
    print("\nCreating customers...")
    
    # Sample customer data
    first_names = ['Ali', 'Fatima', 'Ahmed', 'Ayesha', 'Hassan', 'Zainab', 'Usman', 'Khadija', 
                   'Omar', 'Maryam', 'Ibrahim', 'Sana', 'Bilal', 'Hira', 'Imran']
    last_names = ['Khan', 'Ahmed', 'Ali', 'Hassan', 'Hussain', 'Malik', 'Sheikh', 'Rizvi',
                  'Siddiqui', 'Qureshi', 'Akhtar', 'Butt', 'Chaudhry', 'Raza', 'Iqbal']
    
    customers = []
    
    # Create VIP customers (45 customers, ~45% of base)
    for i in range(45):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name.lower().replace(' ', '.')}vip{i}@example.com"
        
        customer = Customer.objects.create(
            full_name=full_name,
            email=email,
            phone=f"+92-300-{random.randint(1000000, 9999999)}",
            loyalty_tier='VIP',
            is_vip=True,
            lifetime_value=Decimal(random.randint(100000, 500000)),
            total_purchases=random.randint(10, 50),
            average_order_value=Decimal(random.randint(5000, 20000)),
            last_purchase_date=date.today() - timedelta(days=random.randint(1, 30)),
            registration_date=date.today() - timedelta(days=random.randint(180, 730)),
            churn_risk_score=random.randint(0, 20),
            is_at_risk=False,
            is_active=True
        )
        customers.append(customer)
    
    # Create Regular customers (32 customers, ~32%)
    for i in range(32):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name.lower().replace(' ', '.')}regular{i}@example.com"
        
        customer = Customer.objects.create(
            full_name=full_name,
            email=email,
            phone=f"+92-300-{random.randint(1000000, 9999999)}",
            loyalty_tier='REGULAR',
            is_vip=False,
            lifetime_value=Decimal(random.randint(20000, 99999)),
            total_purchases=random.randint(5, 15),
            average_order_value=Decimal(random.randint(2000, 8000)),
            last_purchase_date=date.today() - timedelta(days=random.randint(1, 60)),
            registration_date=date.today() - timedelta(days=random.randint(90, 365)),
            churn_risk_score=random.randint(0, 50),
            is_at_risk=random.choice([True, False]),
            is_active=True
        )
        customers.append(customer)
    
    # Create New Signups (23 customers, ~23%)
    for i in range(23):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name.lower().replace(' ', '.')}new{i}@example.com"
        
        customer = Customer.objects.create(
            full_name=full_name,
            email=email,
            phone=f"+92-300-{random.randint(1000000, 9999999)}",
            loyalty_tier='NEW',
            is_vip=False,
            lifetime_value=Decimal(random.randint(0, 19999)),
            total_purchases=random.randint(0, 4),
            average_order_value=Decimal(random.randint(1000, 5000)),
            last_purchase_date=date.today() - timedelta(days=random.randint(1, 90)) if random.random() > 0.3 else None,
            registration_date=date.today() - timedelta(days=random.randint(1, 90)),
            churn_risk_score=random.randint(0, 30),
            is_at_risk=False,
            is_active=True
        )
        customers.append(customer)
    
    print(f"✓ Created {len(customers)} customers")
    return customers


def create_purchase_records(customers):
    """Create purchase history for customers"""
    print("\nCreating purchase records...")
    
    purchases = []
    payment_methods = ['Cash', 'Card', 'Bank Transfer', 'Mobile Wallet']
    
    for customer in customers:
        num_purchases = customer.total_purchases
        
        for i in range(num_purchases):
            purchase_date = customer.registration_date + timedelta(
                days=random.randint(0, (date.today() - customer.registration_date).days)
            )
            
            purchase = PurchaseRecord.objects.create(
                customer=customer,
                purchase_date=purchase_date,
                amount=Decimal(random.randint(1000, 25000)),
                items_count=random.randint(1, 10),
                payment_method=random.choice(payment_methods)
            )
            purchases.append(purchase)
    
    print(f"✓ Created {len(purchases)} purchase records")
    return purchases


def create_customer_behavior(customers):
    """Create monthly behavior data"""
    print("\nCreating customer behavior data...")
    
    behaviors = []
    
    # Generate for last 6 months
    for i in range(6):
        month_date = date.today() - timedelta(days=30 * i)
        month_str = month_date.strftime('%Y-%m')
        
        for customer in customers:
            # Only create if customer was registered by then
            if customer.registration_date <= month_date:
                behavior = CustomerBehavior.objects.create(
                    customer=customer,
                    month=month_str,
                    purchase_frequency=random.randint(0, 8),
                    total_spent=Decimal(random.randint(0, 50000)),
                    average_days_between_purchases=random.randint(7, 45)
                )
                behaviors.append(behavior)
    
    print(f"✓ Created {len(behaviors)} behavior records")


def create_recent_activities(customers):
    """Create recent activity logs"""
    print("\nCreating recent activities...")
    
    activities = []
    activity_templates = [
        ('SALE', 'New sale record created'),
        ('SALE', 'Purchase completed'),
        ('LEAD_STATUS', 'Lead status: VIP'),
        ('EXPORT', 'Data export requested'),
        ('REGISTRATION', 'New customer registered'),
        ('TIER_CHANGE', 'Upgraded to VIP tier'),
    ]
    
    # Create 15-20 recent activities
    for i in range(random.randint(15, 20)):
        activity_type, description_template = random.choice(activity_templates)
        customer = random.choice(customers) if random.random() > 0.2 else None
        
        hours_ago = random.randint(1, 48)
        activity = RecentActivity.objects.create(
            customer=customer,
            activity_type=activity_type,
            description=description_template,
            metadata={
                'timestamp_hours_ago': hours_ago,
                'amount': str(random.randint(1000, 25000)) if activity_type == 'SALE' else None
            }
        )
        activities.append(activity)
    
    # Manually set timestamps to simulate different times
    for i, activity in enumerate(activities):
        activity.timestamp = datetime.now() - timedelta(hours=random.randint(1, 48))
        activity.save()
    
    print(f"✓ Created {len(activities)} recent activities")


def create_customer_insights():
    """Create AI CRM insights"""
    print("\nCreating customer insights...")
    
    insights = [
        {
            'insight_type': 'SEGMENT',
            'title': 'VIP Customers Growing',
            'description': 'VIP customer segment shows strong growth with 4.2% increase this quarter. '
                          'This tier demonstrates highest engagement and lifetime value.',
            'priority': 'MEDIUM',
            'metric_value': '4.2%',
            'recommendation': 'Maintain engagement with personalized offers and exclusive benefits.',
            'action_plan': {
                'steps': [
                    'Send personalized thank you emails',
                    'Offer exclusive early access to new products',
                    'Provide dedicated customer support line'
                ]
            }
        },
        {
            'insight_type': 'UPSELL',
            'title': 'Upsell Opportunity',
            'description': 'Bundle A recommended for 15% conversion lift. Regular customers showing '
                          'interest in premium products.',
            'priority': 'HIGH',
            'metric_value': '15% lift',
            'recommendation': 'Recommend Bundle A to segment X for 15% conversion lift.',
            'action_plan': {
                'target_segment': 'Regular Customers',
                'estimated_revenue': 'PKR 250,000',
                'timeline': '30 days'
            }
        },
        {
            'insight_type': 'CHURN',
            'title': 'Churn Alert',
            'description': '12 At-Risk accounts detected in Retail segment. These customers have not '
                          'made purchases in 60+ days and show decreased engagement.',
            'priority': 'CRITICAL',
            'metric_value': '12 accounts',
            'recommendation': 'Immediate re-engagement campaign recommended. Offer special discounts '
                            'and personalized outreach.',
            'action_plan': {
                'actions': [
                    'Send win-back email campaign',
                    'Offer 20% discount coupon',
                    'Schedule personal follow-up calls',
                    'Survey to understand pain points'
                ],
                'at_risk_count': 12,
                'potential_loss': 'PKR 540,000'
            }
        },
        {
            'insight_type': 'GROWTH',
            'title': 'Market Expansion',
            'description': 'New customer signups increased by 23% in the last month, indicating '
                          'successful marketing campaigns.',
            'priority': 'MEDIUM',
            'metric_value': '23%',
            'recommendation': 'Continue current marketing strategies and allocate more budget to '
                            'high-performing channels.',
            'action_plan': {
                'focus_areas': [
                    'Social media advertising',
                    'Referral program expansion',
                    'Partnership development'
                ]
            }
        }
    ]
    
    for insight_data in insights:
        CustomerInsight.objects.create(**insight_data)
    
    print(f"✓ Created {len(insights)} customer insights")


def create_kpis():
    """Create current KPI snapshot"""
    print("\nCreating KPIs...")
    
    today = date.today()
    
    # Calculate actual metrics from data
    total_customers = Customer.objects.filter(is_active=True).count()
    
    # Retention rate (customers who purchased in last 90 days)
    ninety_days_ago = today - timedelta(days=90)
    active_customers = Customer.objects.filter(
        is_active=True,
        last_purchase_date__gte=ninety_days_ago
    ).count()
    retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
    
    # Average lifetime value
    from django.db.models import Avg
    avg_ltv = Customer.objects.filter(is_active=True).aggregate(
        avg=Avg('lifetime_value')
    )['avg'] or 0
    
    # Churn risk
    at_risk_count = Customer.objects.filter(is_at_risk=True, is_active=True).count()
    churn_risk = (at_risk_count / total_customers * 100) if total_customers > 0 else 0
    
    # Tier counts
    from django.db.models import Count, Q
    tier_counts = Customer.objects.filter(is_active=True).aggregate(
        vip=Count('id', filter=Q(loyalty_tier='VIP')),
        regular=Count('id', filter=Q(loyalty_tier='REGULAR')),
        new=Count('id', filter=Q(loyalty_tier='NEW')),
    )
    
    kpi = CustomerKPI.objects.create(
        date=today,
        total_customers=total_customers,
        total_customers_change=Decimal('12.0'),  # +12%
        retention_rate=Decimal(str(round(retention_rate, 2))),
        retention_rate_change=Decimal('-2.0'),  # -2%
        avg_lifetime_value=Decimal(str(round(avg_ltv, 2))),
        avg_lifetime_value_change=Decimal('5.0'),  # +5%
        churn_risk_percentage=Decimal(str(round(churn_risk, 2))),
        churn_risk_change=Decimal('-1.0'),  # -1%
        vip_tier_count=tier_counts['vip'],
        regular_tier_count=tier_counts['regular'],
        new_signup_count=tier_counts['new']
    )
    
    print(f"✓ Created KPI snapshot for {today}")
    print(f"  - Total Customers: {kpi.total_customers} (+{kpi.total_customers_change}%)")
    print(f"  - Retention Rate: {kpi.retention_rate}% ({kpi.retention_rate_change}%)")
    print(f"  - Avg Lifetime Value: PKR {kpi.avg_lifetime_value} (+{kpi.avg_lifetime_value_change}%)")
    print(f"  - Churn Risk: {kpi.churn_risk_percentage}% ({kpi.churn_risk_change}%)")


def main():
    """Main execution function"""
    print("=" * 60)
    print("Screen 3: Customer Analytics Data Insertion")
    print("=" * 60)
    
    try:
        clear_existing_data()
        customers = create_customers()
        create_purchase_records(customers)
        create_customer_behavior(customers)
        create_recent_activities(customers)
        create_customer_insights()
        create_kpis()
        
        print("\n" + "=" * 60)
        print("✓ Data insertion completed successfully!")
        print("=" * 60)
        
        # Summary
        print("\nDatabase Summary:")
        print(f"  - Customers: {Customer.objects.count()}")
        print(f"  - Purchase Records: {PurchaseRecord.objects.count()}")
        print(f"  - Customer Behaviors: {CustomerBehavior.objects.count()}")
        print(f"  - Recent Activities: {RecentActivity.objects.count()}")
        print(f"  - Customer Insights: {CustomerInsight.objects.count()}")
        print(f"  - KPIs: {CustomerKPI.objects.count()}")
        
    except Exception as e:
        print(f"\n✗ Error during data insertion: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
