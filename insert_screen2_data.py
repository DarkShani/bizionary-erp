"""
Data Insertion Script for Screen 2: Sales & Items Management
Creates 100+ products with categories, stock history, and sales targets
"""
import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from products.models import Product
from screen_2_sales_items.items_management.models import Category, StockHistory
from screen_2_sales_items.sales_analytics.models import SalesTarget

def create_categories():
    """Create product categories"""
    print("\n=== Creating Categories ===")
    
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Office Supplies', 'description': 'General office supplies and stationery'},
        {'name': 'Furniture', 'description': 'Office and home furniture'},
        {'name': 'Computer Accessories', 'description': 'Computer peripherals and accessories'},
        {'name': 'Networking Equipment', 'description': 'Network devices and cables'},
        {'name': 'Office Equipment', 'description': 'Printers, scanners, and office machines'},
        {'name': 'Storage Solutions', 'description': 'Storage devices and solutions'},
        {'name': 'Audio Visual', 'description': 'Audio and visual equipment'},
        {'name': 'Software & Licenses', 'description': 'Software products and licenses'},
        {'name': 'Stationery', 'description': 'Writing and paper products'},
    ]
    
    created_count = 0
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            created_count += 1
            print(f"  ✓ Created: {category.name}")
        else:
            print(f"  - Exists: {category.name}")
    
    print(f"\nCategories: {created_count} created, {len(categories_data) - created_count} already existed")
    return Category.objects.all()


def create_products():
    """Create 100+ diverse products"""
    print("\n=== Creating Products ===")
    
    products_data = [
        # Electronics (20 products)
        ('Wireless Mouse Logitech M185', 'WM-001', 'Electronics', 1500.00, 85, 15),
        ('Wireless Keyboard K380', 'WK-002', 'Electronics', 3500.00, 60, 10),
        ('USB Wired Mouse', 'UM-003', 'Electronics', 500.00, 120, 20),
        ('Mechanical Keyboard RGB', 'MK-004', 'Electronics', 8500.00, 35, 5),
        ('Gaming Mouse RGB', 'GM-005', 'Electronics', 4500.00, 45, 8),
        ('Bluetooth Headphones', 'BH-006', 'Electronics', 2500.00, 70, 12),
        ('USB-C Hub 7-in-1', 'UH-007', 'Electronics', 3200.00, 55, 10),
        ('Webcam 1080p HD', 'WC-008', 'Electronics', 4800.00, 40, 8),
        ('USB Microphone', 'UM-009', 'Electronics', 3800.00, 30, 5),
        ('LED Desk Lamp', 'LD-010', 'Electronics', 2200.00, 65, 12),
        ('Power Bank 20000mAh', 'PB-011', 'Electronics', 2800.00, 90, 15),
        ('USB Flash Drive 64GB', 'FD-012', 'Electronics', 800.00, 150, 25),
        ('External HDD 1TB', 'HD-013', 'Electronics', 5500.00, 45, 8),
        ('SSD External 500GB', 'SD-014', 'Electronics', 6500.00, 35, 6),
        ('HDMI Cable 2m', 'HC-015', 'Electronics', 350.00, 200, 30),
        ('USB-C Cable 1.5m', 'UC-016', 'Electronics', 450.00, 180, 30),
        ('Phone Stand Adjustable', 'PS-017', 'Electronics', 1200.00, 75, 12),
        ('Laptop Cooling Pad', 'LP-018', 'Electronics', 1800.00, 50, 10),
        ('Monitor Stand Riser', 'MS-019', 'Electronics', 2500.00, 40, 8),
        ('Cable Management Box', 'CB-020', 'Electronics', 900.00, 85, 15),
        
        # Office Supplies (25 products)
        ('A4 Copy Paper 500 Sheets', 'CP-021', 'Office Supplies', 500.00, 300, 50),
        ('A4 Colored Paper Pack', 'CP-022', 'Office Supplies', 350.00, 150, 25),
        ('Stapler Heavy Duty', 'ST-023', 'Office Supplies', 850.00, 60, 10),
        ('Staples Box 5000pcs', 'SB-024', 'Office Supplies', 250.00, 200, 30),
        ('Paper Clips Box 100pcs', 'PC-025', 'Office Supplies', 120.00, 180, 30),
        ('Binder Clips Assorted', 'BC-026', 'Office Supplies', 200.00, 150, 25),
        ('Sticky Notes 3x3 Pack', 'SN-027', 'Office Supplies', 180.00, 250, 40),
        ('Whiteboard Markers Set', 'WM-028', 'Office Supplies', 450.00, 120, 20),
        ('Permanent Markers Black', 'PM-029', 'Office Supplies', 280.00, 140, 25),
        ('Highlighter Set 4 Colors', 'HS-030', 'Office Supplies', 320.00, 160, 25),
        ('Ballpoint Pen Blue Box', 'BP-031', 'Office Supplies', 400.00, 200, 35),
        ('Gel Pen Set 12 Colors', 'GP-032', 'Office Supplies', 550.00, 90, 15),
        ('Pencil HB Box 12pcs', 'PE-033', 'Office Supplies', 180.00, 170, 30),
        ('Eraser White Large', 'ER-034', 'Office Supplies', 50.00, 250, 40),
        ('Ruler 30cm Plastic', 'RU-035', 'Office Supplies', 80.00, 200, 35),
        ('Scissors 8 inch', 'SC-036', 'Office Supplies', 250.00, 110, 20),
        ('Tape Dispenser Desktop', 'TD-037', 'Office Supplies', 350.00, 80, 15),
        ('Clear Tape Roll 24mm', 'CT-038', 'Office Supplies', 120.00, 220, 40),
        ('Glue Stick 40g', 'GS-039', 'Office Supplies', 90.00, 180, 30),
        ('File Folder A4 Pack 10', 'FF-040', 'Office Supplies', 280.00, 140, 25),
        ('Ring Binder A4 4-Ring', 'RB-041', 'Office Supplies', 420.00, 95, 15),
        ('Document Tray 3-Tier', 'DT-042', 'Office Supplies', 1200.00, 45, 8),
        ('Desk Organizer 5-Slot', 'DO-043', 'Office Supplies', 850.00, 55, 10),
        ('Puncher 2-Hole Heavy', 'PH-044', 'Office Supplies', 650.00, 70, 12),
        ('Calendar Desk 2026', 'CD-045', 'Office Supplies', 380.00, 120, 20),
        
        # Furniture (15 products)
        ('Office Chair Ergonomic', 'OC-046', 'Furniture', 15000.00, 25, 5),
        ('Executive Chair Leather', 'EC-047', 'Furniture', 28000.00, 15, 3),
        ('Computer Desk 120cm', 'CD-048', 'Furniture', 18000.00, 20, 4),
        ('Standing Desk Adjustable', 'SD-049', 'Furniture', 35000.00, 10, 2),
        ('Bookshelf 5-Tier', 'BS-050', 'Furniture', 12000.00, 18, 3),
        ('Filing Cabinet 4-Drawer', 'FC-051', 'Furniture', 22000.00, 12, 2),
        ('Meeting Table 6-Seater', 'MT-052', 'Furniture', 45000.00, 8, 2),
        ('Reception Desk Modern', 'RD-053', 'Furniture', 38000.00, 6, 1),
        ('Waiting Chair Set 3pcs', 'WC-054', 'Furniture', 18000.00, 14, 3),
        ('Coffee Table Glass Top', 'CT-055', 'Furniture', 12500.00, 16, 3),
        ('Storage Cabinet Metal', 'SC-056', 'Furniture', 16000.00, 11, 2),
        ('Whiteboard Mobile 120cm', 'WB-057', 'Furniture', 8500.00, 22, 4),
        ('Notice Board Cork 90cm', 'NB-058', 'Furniture', 3200.00, 28, 5),
        ('Coat Rack Floor Stand', 'CR-059', 'Furniture', 2800.00, 35, 6),
        ('Footrest Adjustable', 'FR-060', 'Furniture', 1800.00, 40, 8),
        
        # Computer Accessories (20 products)
        ('Laptop Bag 15.6 inch', 'LB-061', 'Computer Accessories', 2500.00, 65, 12),
        ('Laptop Sleeve 14 inch', 'LS-062', 'Computer Accessories', 1200.00, 80, 15),
        ('Mouse Pad Gaming XXL', 'MP-063', 'Computer Accessories', 1500.00, 90, 15),
        ('Keyboard Wrist Rest', 'KW-064', 'Computer Accessories', 800.00, 70, 12),
        ('Screen Protector 15.6', 'SP-065', 'Computer Accessories', 650.00, 100, 18),
        ('Privacy Filter 14 inch', 'PF-066', 'Computer Accessories', 2200.00, 45, 8),
        ('USB Hub 4-Port', 'UH-067', 'Computer Accessories', 850.00, 110, 20),
        ('Card Reader SD/MicroSD', 'CR-068', 'Computer Accessories', 550.00, 95, 16),
        ('Laptop Stand Aluminum', 'LS-069', 'Computer Accessories', 3200.00, 50, 10),
        ('Monitor Arm Single', 'MA-070', 'Computer Accessories', 5500.00, 30, 5),
        ('Keyboard Cover Silicone', 'KC-071', 'Computer Accessories', 350.00, 120, 20),
        ('Cleaning Kit PC', 'CK-072', 'Computer Accessories', 650.00, 85, 15),
        ('Compressed Air Duster', 'AD-073', 'Computer Accessories', 450.00, 100, 18),
        ('Cable Ties Pack 100pcs', 'CT-074', 'Computer Accessories', 280.00, 150, 25),
        ('VGA Cable 3m', 'VC-075', 'Computer Accessories', 420.00, 95, 16),
        ('DisplayPort Cable 2m', 'DC-076', 'Computer Accessories', 850.00, 70, 12),
        ('USB Extension 3m', 'UE-077', 'Computer Accessories', 380.00, 110, 20),
        ('Audio Splitter 3.5mm', 'AS-078', 'Computer Accessories', 250.00, 130, 22),
        ('Headphone Stand', 'HS-079', 'Computer Accessories', 1200.00, 60, 10),
        ('RAM Cooling Fan RGB', 'RF-080', 'Computer Accessories', 1800.00, 40, 8),
        
        # Networking Equipment (10 products)
        ('Ethernet Cable Cat6 5m', 'EC-081', 'Networking Equipment', 450.00, 180, 30),
        ('Ethernet Cable Cat6 10m', 'EC-082', 'Networking Equipment', 750.00, 120, 20),
        ('RJ45 Connector Pack 50', 'RJ-083', 'Networking Equipment', 550.00, 100, 18),
        ('Network Switch 8-Port', 'NS-084', 'Networking Equipment', 3500.00, 35, 6),
        ('WiFi Router Dual Band', 'WR-085', 'Networking Equipment', 6500.00, 28, 5),
        ('WiFi Extender', 'WE-086', 'Networking Equipment', 3200.00, 45, 8),
        ('Patch Panel 24-Port', 'PP-087', 'Networking Equipment', 5500.00, 22, 4),
        ('Cable Tester RJ45', 'CT-088', 'Networking Equipment', 1200.00, 38, 7),
        ('Network Cable Organizer', 'CO-089', 'Networking Equipment', 850.00, 55, 10),
        ('Fiber Optic Cable 10m', 'FC-090', 'Networking Equipment', 2800.00, 30, 5),
        
        # Office Equipment (8 products)
        ('Printer Laser Mono A4', 'PL-091', 'Office Equipment', 18500.00, 20, 4),
        ('Printer Inkjet Color', 'PI-092', 'Office Equipment', 12000.00, 25, 5),
        ('Scanner Flatbed A4', 'SF-093', 'Office Equipment', 9500.00, 18, 3),
        ('Laminator A4 Hot/Cold', 'LA-094', 'Office Equipment', 6500.00, 28, 5),
        ('Paper Shredder Cross', 'PS-095', 'Office Equipment', 8500.00, 22, 4),
        ('Label Maker Portable', 'LM-096', 'Office Equipment', 3500.00, 35, 6),
        ('Binding Machine Comb', 'BM-097', 'Office Equipment', 5500.00, 24, 4),
        ('Calculator Desktop 12D', 'CA-098', 'Office Equipment', 850.00, 80, 15),
        
        # Additional products to reach 100+
        ('Toner Cartridge HP Black', 'TC-099', 'Office Equipment', 5500.00, 45, 8),
        ('Ink Cartridge Epson Set', 'IC-100', 'Office Equipment', 3800.00, 60, 10),
    ]
    
    created_count = 0
    updated_count = 0
    
    for name, sku, category, price, stock, reorder in products_data:
        product, created = Product.objects.update_or_create(
            sku=sku,
            defaults={
                'name': name,
                'category': category,
                'unit_price': Decimal(str(price)),
                'stock_quantity': stock,
                'reorder_level': reorder,
                'description': f'{name} - High quality product for office and business use'
            }
        )
        
        if created:
            created_count += 1
            print(f"  ✓ Created: {name} ({sku})")
            
            # Create initial stock history
            StockHistory.objects.create(
                product=product,
                transaction_type='PURCHASE',
                quantity_change=stock,
                quantity_after=stock,
                reference_id=f'INITIAL-{sku}',
                notes='Initial stock on product creation',
                created_by='system'
            )
        else:
            updated_count += 1
            print(f"  ↻ Updated: {name} ({sku})")
    
    print(f"\nProducts: {created_count} created, {updated_count} updated")
    return Product.objects.all()


def create_stock_movements():
    """Create realistic stock history for products"""
    print("\n=== Creating Stock History ===")
    
    products = Product.objects.all()
    transaction_types = ['SALE', 'PURCHASE', 'ADJUSTMENT', 'RETURN', 'DAMAGE']
    
    created_count = 0
    
    # Create 200 random stock movements over the past 3 months
    for _ in range(200):
        product = random.choice(products)
        trans_type = random.choice(transaction_types)
        
        # Determine quantity change based on transaction type
        if trans_type in ['SALE', 'DAMAGE']:
            quantity_change = -random.randint(1, 10)
        elif trans_type == 'PURCHASE':
            quantity_change = random.randint(10, 50)
        elif trans_type == 'RETURN':
            quantity_change = random.randint(1, 5)
        else:  # ADJUSTMENT
            quantity_change = random.randint(-5, 15)
        
        # Calculate new stock
        new_stock = max(0, product.stock_quantity + quantity_change)
        
        # Create history entry with past date
        days_ago = random.randint(1, 90)
        created_date = datetime.now() - timedelta(days=days_ago)
        
        history = StockHistory.objects.create(
            product=product,
            transaction_type=trans_type,
            quantity_change=quantity_change,
            quantity_after=new_stock,
            reference_id=f'{trans_type}-{random.randint(1000, 9999)}',
            notes=f'{trans_type} transaction',
            created_by=random.choice(['admin', 'warehouse_user', 'system'])
        )
        history.created_at = created_date
        history.save()
        
        created_count += 1
    
    print(f"  ✓ Created {created_count} stock history entries")


def create_sales_targets():
    """Create sales targets for next 6 months"""
    print("\n=== Creating Sales Targets ===")
    
    created_count = 0
    today = datetime.now().date()
    
    # Monthly targets for next 6 months
    for month_offset in range(6):
        start_date = (today.replace(day=1) + timedelta(days=32 * month_offset)).replace(day=1)
        # Last day of month
        if start_date.month == 12:
            end_date = start_date.replace(day=31)
        else:
            end_date = (start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1))
        
        target, created = SalesTarget.objects.get_or_create(
            period_type='MONTHLY',
            start_date=start_date,
            end_date=end_date,
            defaults={
                'target_amount': Decimal(str(random.randint(500000, 800000))),
                'target_units': random.randint(1500, 2500),
                'notes': f'Monthly target for {start_date.strftime("%B %Y")}'
            }
        )
        
        if created:
            created_count += 1
            print(f"  ✓ Created target for {start_date.strftime('%B %Y')}: Rs {target.target_amount}")
    
    # Quarterly target
    q_start = today.replace(month=1, day=1)
    q_end = today.replace(month=3, day=31)
    
    target, created = SalesTarget.objects.get_or_create(
        period_type='QUARTERLY',
        start_date=q_start,
        end_date=q_end,
        defaults={
            'target_amount': Decimal('2000000'),
            'target_units': 6000,
            'notes': 'Q1 2026 Target'
        }
    )
    
    if created:
        created_count += 1
        print(f"  ✓ Created quarterly target: Rs {target.target_amount}")
    
    print(f"\nSales Targets: {created_count} created")


def print_summary():
    """Print summary of all data"""
    print("\n" + "="*70)
    print("DATA INSERTION SUMMARY")
    print("="*70)
    
    categories_count = Category.objects.count()
    products_count = Product.objects.count()
    stock_history_count = StockHistory.objects.count()
    sales_targets_count = SalesTarget.objects.count()
    
    print(f"\nCategories:      {categories_count}")
    print(f"Products:        {products_count}")
    print(f"Stock History:   {stock_history_count}")
    print(f"Sales Targets:   {sales_targets_count}")
    
    # Top 5 categories by product count
    print("\n--- Top Categories ---")
    from django.db.models import Count
    top_categories = Product.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    for cat in top_categories:
        print(f"  {cat['category']}: {cat['count']} products")
    
    # Stock status summary
    low_stock = Product.objects.filter(stock_quantity__lte=models.F('reorder_level')).count()
    out_of_stock = Product.objects.filter(stock_quantity=0).count()
    in_stock = products_count - low_stock
    
    print("\n--- Stock Status ---")
    print(f"  In Stock:      {in_stock}")
    print(f"  Low Stock:     {low_stock}")
    print(f"  Out of Stock:  {out_of_stock}")
    
    print("\n" + "="*70)
    print("✓ All data inserted successfully!")
    print("="*70)


if __name__ == '__main__':
    print("="*70)
    print("SCREEN 2 DATA INSERTION SCRIPT")
    print("Sales & Items Management")
    print("="*70)
    
    from django.db import models
    
    try:
        # Step 1: Create categories
        create_categories()
        
        # Step 2: Create products
        create_products()
        
        # Step 3: Create stock movements
        create_stock_movements()
        
        # Step 4: Create sales targets
        create_sales_targets()
        
        # Step 5: Print summary
        print_summary()
        
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
