"""
Screen 4: Accounts & Finance - Dummy Data Generator
Script to insert predefined revenue, expense, and invoice data
Run with: python insert_screen4_data.py
"""

import os
import sys
import django
from datetime import datetime
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from accounts.models import Revenue, Expense, Invoice


def insert_revenues():
    """Insert predefined revenue data for the last 6 months"""
    print("Inserting Revenue data...")
    
    # Realistic revenue data spanning August 2025 to January 2026
    revenues_data_list = [
        # August 2025
        {'source': 'Product Sales', 'amount': Decimal('145000.00'), 'date': '2025-08-05', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('85000.00'), 'date': '2025-08-12', 'description': 'Consulting and support services'},
        {'source': 'Subscription Revenue', 'amount': Decimal('45000.00'), 'date': '2025-08-20', 'description': 'Monthly subscription renewals'},
        {'source': 'Commission Income', 'amount': Decimal('28000.00'), 'date': '2025-08-25', 'description': 'Partner commission earnings'},
        
        # September 2025
        {'source': 'Product Sales', 'amount': Decimal('165000.00'), 'date': '2025-09-03', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('92000.00'), 'date': '2025-09-10', 'description': 'Consulting and support services'},
        {'source': 'License Revenue', 'amount': Decimal('120000.00'), 'date': '2025-09-15', 'description': 'Software licensing fees'},
        {'source': 'Subscription Revenue', 'amount': Decimal('48000.00'), 'date': '2025-09-22', 'description': 'Monthly subscription renewals'},
        {'source': 'Commission Income', 'amount': Decimal('32000.00'), 'date': '2025-09-28', 'description': 'Partner commission earnings'},
        
        # October 2025
        {'source': 'Product Sales', 'amount': Decimal('178000.00'), 'date': '2025-10-05', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('98000.00'), 'date': '2025-10-12', 'description': 'Consulting and support services'},
        {'source': 'Subscription Revenue', 'amount': Decimal('52000.00'), 'date': '2025-10-18', 'description': 'Monthly subscription renewals'},
        {'source': 'Rental Income', 'amount': Decimal('25000.00'), 'date': '2025-10-20', 'description': 'Equipment rental services'},
        {'source': 'Commission Income', 'amount': Decimal('35000.00'), 'date': '2025-10-26', 'description': 'Partner commission earnings'},
        
        # November 2025
        {'source': 'Product Sales', 'amount': Decimal('195000.00'), 'date': '2025-11-04', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('105000.00'), 'date': '2025-11-11', 'description': 'Consulting and support services'},
        {'source': 'License Revenue', 'amount': Decimal('135000.00'), 'date': '2025-11-16', 'description': 'Software licensing fees'},
        {'source': 'Subscription Revenue', 'amount': Decimal('55000.00'), 'date': '2025-11-21', 'description': 'Monthly subscription renewals'},
        {'source': 'Interest Income', 'amount': Decimal('8000.00'), 'date': '2025-11-25', 'description': 'Bank interest earnings'},
        {'source': 'Commission Income', 'amount': Decimal('38000.00'), 'date': '2025-11-28', 'description': 'Partner commission earnings'},
        
        # December 2025
        {'source': 'Product Sales', 'amount': Decimal('210000.00'), 'date': '2025-12-05', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('112000.00'), 'date': '2025-12-10', 'description': 'Consulting and support services'},
        {'source': 'Subscription Revenue', 'amount': Decimal('58000.00'), 'date': '2025-12-18', 'description': 'Monthly subscription renewals'},
        {'source': 'Rental Income', 'amount': Decimal('30000.00'), 'date': '2025-12-22', 'description': 'Equipment rental services'},
        {'source': 'Commission Income', 'amount': Decimal('42000.00'), 'date': '2025-12-28', 'description': 'Partner commission earnings'},
        
        # January 2026
        {'source': 'Product Sales', 'amount': Decimal('188000.00'), 'date': '2026-01-06', 'description': 'Monthly product sales revenue'},
        {'source': 'Service Income', 'amount': Decimal('102000.00'), 'date': '2026-01-13', 'description': 'Consulting and support services'},
        {'source': 'License Revenue', 'amount': Decimal('140000.00'), 'date': '2026-01-17', 'description': 'Software licensing fees'},
        {'source': 'Subscription Revenue', 'amount': Decimal('60000.00'), 'date': '2026-01-22', 'description': 'Monthly subscription renewals'},
        {'source': 'Interest Income', 'amount': Decimal('9000.00'), 'date': '2026-01-28', 'description': 'Bank interest earnings'},
        {'source': 'Commission Income', 'amount': Decimal('40000.00'), 'date': '2026-01-30', 'description': 'Partner commission earnings'},
    ]
    
    revenues_data = []
    for item in revenues_data_list:
        revenue = Revenue(
            source=item['source'],
            amount=item['amount'],
            date=datetime.strptime(item['date'], '%Y-%m-%d').date(),
            description=item['description']
        )
        revenues_data.append(revenue)
    
    Revenue.objects.bulk_create(revenues_data)
    print(f"✓ Inserted {len(revenues_data)} revenue records")


def insert_expenses():
    """Insert predefined expense data for the last 6 months"""
    print("Inserting Expense data...")
    
    # Realistic expense data spanning August 2025 to January 2026
    expenses_data_list = [
        # August 2025
        {'category': 'PAYROLL', 'amount': Decimal('85000.00'), 'date': '2025-08-01', 'vendor': 'Internal HR Department', 'description': 'Monthly salary disbursement'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('28000.00'), 'date': '2025-08-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('35000.00'), 'date': '2025-08-10', 'vendor': 'Digital Marketing Agency', 'description': 'Social media and online advertising'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('15000.00'), 'date': '2025-08-15', 'vendor': 'Cloud Services Ltd', 'description': 'AWS and software subscriptions'},
        {'category': 'SUPPLIES', 'amount': Decimal('8500.00'), 'date': '2025-08-20', 'vendor': 'Office Depot', 'description': 'Office supplies and stationery'},
        {'category': 'TRAVEL', 'amount': Decimal('12000.00'), 'date': '2025-08-25', 'vendor': 'Corporate Travel Services', 'description': 'Business travel expenses'},
        
        # September 2025
        {'category': 'PAYROLL', 'amount': Decimal('87000.00'), 'date': '2025-09-01', 'vendor': 'Internal HR Department', 'description': 'Monthly salary disbursement'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('28500.00'), 'date': '2025-09-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('42000.00'), 'date': '2025-09-08', 'vendor': 'Digital Marketing Agency', 'description': 'Campaign launch and advertising'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('18000.00'), 'date': '2025-09-12', 'vendor': 'Tech Solutions Inc', 'description': 'Software licenses and IT infrastructure'},
        {'category': 'SUPPLIES', 'amount': Decimal('9000.00'), 'date': '2025-09-18', 'vendor': 'Office Depot', 'description': 'Office supplies and equipment'},
        {'category': 'OTHER', 'amount': Decimal('5500.00'), 'date': '2025-09-25', 'vendor': 'Legal Advisors LLP', 'description': 'Legal consultation fees'},
        
        # October 2025
        {'category': 'PAYROLL', 'amount': Decimal('89000.00'), 'date': '2025-10-01', 'vendor': 'Internal HR Department', 'description': 'Monthly salary disbursement'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('29000.00'), 'date': '2025-10-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('38000.00'), 'date': '2025-10-10', 'vendor': 'Digital Marketing Agency', 'description': 'Marketing campaigns'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('16500.00'), 'date': '2025-10-14', 'vendor': 'Cloud Services Ltd', 'description': 'Cloud hosting and SaaS tools'},
        {'category': 'SUPPLIES', 'amount': Decimal('7800.00'), 'date': '2025-10-20', 'vendor': 'ABC Suppliers', 'description': 'Office and operational supplies'},
        {'category': 'TRAVEL', 'amount': Decimal('15000.00'), 'date': '2025-10-28', 'vendor': 'Travel Agency Pro', 'description': 'Client meetings and conferences'},
        
        # November 2025
        {'category': 'PAYROLL', 'amount': Decimal('92000.00'), 'date': '2025-11-01', 'vendor': 'Internal HR Department', 'description': 'Monthly salary disbursement'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('29500.00'), 'date': '2025-11-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('45000.00'), 'date': '2025-11-09', 'vendor': 'Global Marketing Agency', 'description': 'Holiday season marketing push'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('19000.00'), 'date': '2025-11-13', 'vendor': 'Tech Solutions Inc', 'description': 'System upgrades and maintenance'},
        {'category': 'SUPPLIES', 'amount': Decimal('9500.00'), 'date': '2025-11-18', 'vendor': 'Office Depot', 'description': 'Supplies and equipment purchases'},
        {'category': 'OTHER', 'amount': Decimal('6000.00'), 'date': '2025-11-22', 'vendor': 'Insurance Brokers Inc', 'description': 'Business insurance premium'},
        {'category': 'TRAVEL', 'amount': Decimal('13500.00'), 'date': '2025-11-27', 'vendor': 'Corporate Travel Services', 'description': 'Business travel and accommodation'},
        
        # December 2025
        {'category': 'PAYROLL', 'amount': Decimal('95000.00'), 'date': '2025-12-01', 'vendor': 'Internal HR Department', 'description': 'Monthly salary with bonuses'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('30000.00'), 'date': '2025-12-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('52000.00'), 'date': '2025-12-08', 'vendor': 'Digital Marketing Agency', 'description': 'Year-end promotional campaigns'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('22000.00'), 'date': '2025-12-12', 'vendor': 'Cloud Services Ltd', 'description': 'Annual software renewals'},
        {'category': 'SUPPLIES', 'amount': Decimal('11000.00'), 'date': '2025-12-16', 'vendor': 'ABC Suppliers', 'description': 'Year-end supplies and inventory'},
        {'category': 'OTHER', 'amount': Decimal('8000.00'), 'date': '2025-12-20', 'vendor': 'Event Management Co', 'description': 'Company year-end event'},
        {'category': 'TRAVEL', 'amount': Decimal('10000.00'), 'date': '2025-12-28', 'vendor': 'Travel Agency Pro', 'description': 'Business travel expenses'},
        
        # January 2026
        {'category': 'PAYROLL', 'amount': Decimal('90000.00'), 'date': '2026-01-02', 'vendor': 'Internal HR Department', 'description': 'Monthly salary disbursement'},
        {'category': 'RENT_UTILITIES', 'amount': Decimal('30500.00'), 'date': '2026-01-05', 'vendor': 'City Property Management', 'description': 'Office rent and utilities'},
        {'category': 'MARKETING', 'amount': Decimal('40000.00'), 'date': '2026-01-10', 'vendor': 'Digital Marketing Agency', 'description': 'New year marketing campaigns'},
        {'category': 'TECHNOLOGY', 'amount': Decimal('17500.00'), 'date': '2026-01-15', 'vendor': 'Tech Solutions Inc', 'description': 'IT services and cloud hosting'},
        {'category': 'SUPPLIES', 'amount': Decimal('8800.00'), 'date': '2026-01-20', 'vendor': 'Office Depot', 'description': 'Office supplies restocking'},
        {'category': 'OTHER', 'amount': Decimal('5000.00'), 'date': '2026-01-25', 'vendor': 'Professional Services', 'description': 'Consulting and advisory fees'},
        {'category': 'TRAVEL', 'amount': Decimal('14000.00'), 'date': '2026-01-30', 'vendor': 'Corporate Travel Services', 'description': 'International business meetings'},
    ]
    
    expenses_data = []
    for item in expenses_data_list:
        expense = Expense(
            category=item['category'],
            amount=item['amount'],
            date=datetime.strptime(item['date'], '%Y-%m-%d').date(),
            vendor=item['vendor'],
            description=item['description']
        )
        expenses_data.append(expense)
    
    Expense.objects.bulk_create(expenses_data)
    print(f"✓ Inserted {len(expenses_data)} expense records")


def insert_invoices():
    """Insert predefined invoices"""
    print("Inserting Invoice data...")
    
    # Realistic invoice data
    invoices_data_list = [
        {'invoice_number': 'INV-0082', 'client_name': 'TechNow Solutions', 'amount': Decimal('45000.00'), 'status': 'PAID', 'due_date': '2024-10-28', 'created_at': '2024-10-01', 'description': 'Software development services - Q3 2024'},
        {'invoice_number': 'INV-0081', 'client_name': 'Creative Agency', 'amount': Decimal('120000.00'), 'status': 'PENDING', 'due_date': '2024-11-02', 'created_at': '2024-10-05', 'description': 'Digital marketing campaign management'},
        {'invoice_number': 'INV-0080', 'client_name': 'Global Logistics', 'amount': Decimal('32500.00'), 'status': 'OVERDUE', 'due_date': '2024-10-20', 'created_at': '2024-09-20', 'description': 'Supply chain optimization consulting'},
        {'invoice_number': 'INV-0083', 'client_name': 'Digital Marketing Pro', 'amount': Decimal('85000.00'), 'status': 'PAID', 'due_date': '2024-11-15', 'created_at': '2024-10-18', 'description': 'Social media management services'},
        {'invoice_number': 'INV-0084', 'client_name': 'Enterprise Software Inc', 'amount': Decimal('150000.00'), 'status': 'PAID', 'due_date': '2024-11-25', 'created_at': '2024-10-28', 'description': 'Enterprise software licensing - Annual'},
        {'invoice_number': 'INV-0085', 'client_name': 'Healthcare Systems', 'amount': Decimal('95000.00'), 'status': 'PENDING', 'due_date': '2024-12-05', 'created_at': '2024-11-05', 'description': 'Healthcare management system implementation'},
        {'invoice_number': 'INV-0086', 'client_name': 'Financial Services Ltd', 'amount': Decimal('68000.00'), 'status': 'PAID', 'due_date': '2024-12-10', 'created_at': '2024-11-12', 'description': 'Financial data analytics solution'},
        {'invoice_number': 'INV-0087', 'client_name': 'Retail Chain Co', 'amount': Decimal('42000.00'), 'status': 'PENDING', 'due_date': '2024-12-20', 'created_at': '2024-11-22', 'description': 'Point of sale system upgrade'},
        {'invoice_number': 'INV-0088', 'client_name': 'Manufacturing Corp', 'amount': Decimal('178000.00'), 'status': 'PAID', 'due_date': '2025-01-08', 'created_at': '2024-12-10', 'description': 'ERP system customization and support'},
        {'invoice_number': 'INV-0089', 'client_name': 'Education Platform', 'amount': Decimal('55000.00'), 'status': 'OVERDUE', 'due_date': '2024-12-28', 'created_at': '2024-11-28', 'description': 'E-learning platform development'},
        {'invoice_number': 'INV-0090', 'client_name': 'TechNow Solutions', 'amount': Decimal('72000.00'), 'status': 'PAID', 'due_date': '2025-01-15', 'created_at': '2024-12-18', 'description': 'Mobile app development - Phase 2'},
        {'invoice_number': 'INV-0091', 'client_name': 'Global Logistics', 'amount': Decimal('48000.00'), 'status': 'PENDING', 'due_date': '2025-01-25', 'created_at': '2024-12-28', 'description': 'Logistics tracking system integration'},
        {'invoice_number': 'INV-0092', 'client_name': 'Creative Agency', 'amount': Decimal('135000.00'), 'status': 'PENDING', 'due_date': '2025-02-05', 'created_at': '2025-01-08', 'description': 'Brand identity and design services'},
    ]
    
    invoices_data = []
    for item in invoices_data_list:
        created_dt = datetime.strptime(item['created_at'], '%Y-%m-%d')
        invoice = Invoice(
            invoice_number=item['invoice_number'],
            client_name=item['client_name'],
            amount=item['amount'],
            status=item['status'],
            due_date=datetime.strptime(item['due_date'], '%Y-%m-%d').date(),
            description=item['description'],
            created_at=created_dt
        )
        invoices_data.append(invoice)
    
    # Save each invoice to preserve created_at timestamp
    for invoice in invoices_data:
        invoice.save()
    
    print(f"✓ Inserted {len(invoices_data)} invoice records")


def clear_existing_data():
    """Clear existing data (optional - use with caution)"""
    print("Clearing existing Screen 4 data...")
    Revenue.objects.all().delete()
    Expense.objects.all().delete()
    Invoice.objects.all().delete()
    print("✓ Cleared all existing data")


def main():
    """Main function to run the data insertion"""
    print("=" * 60)
    print("Screen 4: Accounts & Finance - Data Generator")
    print("=" * 60)
    print()
    
    # Ask user if they want to clear existing data
    clear_data = input("Clear existing data? (y/n): ").lower().strip()
    if clear_data == 'y':
        clear_existing_data()
        print()
    
    try:
        # Insert data
        insert_revenues()
        insert_expenses()
        insert_invoices()
        
        print()
        print("=" * 60)
        print("✓ SUCCESS! All data inserted successfully")
        print("=" * 60)
        print()
        
        # Print summary
        print("DATA SUMMARY:")
        print(f"Total Revenues: {Revenue.objects.count()}")
        print(f"Total Expenses: {Expense.objects.count()}")
        print(f"Total Invoices: {Invoice.objects.count()}")
        print()
        
        # Print some statistics
        from django.db.models import Sum
        total_revenue = Revenue.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        net_profit = total_revenue - total_expense
        
        print("FINANCIAL SUMMARY:")
        print(f"Total Revenue: Rs. {total_revenue:,.2f}")
        print(f"Total Expense: Rs. {total_expense:,.2f}")
        print(f"Net Profit: Rs. {net_profit:,.2f}")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR occurred during data insertion")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
