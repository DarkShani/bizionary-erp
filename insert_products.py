#!/usr/bin/env python
"""Seed products using only initial_products_data (SKU051-SKU100)."""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from products.models import Product

# ===== PRODUCT DATA =====
initial_products_data = [
    {'name': 'A4 Copy Paper 100 GSM', 'sku': 'SKU051', 'category': 'Copy Paper', 'unit_price': Decimal('10.00'), 'stock_quantity': 60},
    {'name': 'A3 Copy Paper 100 GSM', 'sku': 'SKU052', 'category': 'Copy Paper', 'unit_price': Decimal('12.00'), 'stock_quantity': 50},
    {'name': 'A5 Colored Paper Yellow', 'sku': 'SKU053', 'category': 'Copy Paper', 'unit_price': Decimal('7.50'), 'stock_quantity': 70},
    {'name': 'A5 Colored Paper Pink', 'sku': 'SKU054', 'category': 'Copy Paper', 'unit_price': Decimal('7.50'), 'stock_quantity': 65},
    {'name': 'A4 Sticker Paper', 'sku': 'SKU055', 'category': 'Office Supplies', 'unit_price': Decimal('9.00'), 'stock_quantity': 40},
    {'name': 'A3 Sticker Paper', 'sku': 'SKU056', 'category': 'Office Supplies', 'unit_price': Decimal('11.00'), 'stock_quantity': 35},
    {'name': 'Glossy Photo Paper A3', 'sku': 'SKU057', 'category': 'Photo Paper', 'unit_price': Decimal('18.00'), 'stock_quantity': 20},
    {'name': 'Matte Photo Paper A3', 'sku': 'SKU058', 'category': 'Photo Paper', 'unit_price': Decimal('17.00'), 'stock_quantity': 25},
    {'name': 'Premium Card Stock 120 GSM', 'sku': 'SKU059', 'category': 'Photo Paper', 'unit_price': Decimal('13.00'), 'stock_quantity': 45},
    {'name': 'Recycled Copy Paper A4', 'sku': 'SKU060', 'category': 'Copy Paper', 'unit_price': Decimal('6.00'), 'stock_quantity': 90},
    {'name': 'Recycled Copy Paper A3', 'sku': 'SKU061', 'category': 'Copy Paper', 'unit_price': Decimal('7.00'), 'stock_quantity': 80},
    {'name': 'Office Writing Pad A4', 'sku': 'SKU062', 'category': 'Notebook', 'unit_price': Decimal('2.50'), 'stock_quantity': 150},
    {'name': 'Office Writing Pad A5', 'sku': 'SKU063', 'category': 'Notebook', 'unit_price': Decimal('2.00'), 'stock_quantity': 170},
    {'name': 'Executive Notebook Leather', 'sku': 'SKU064', 'category': 'Notebook', 'unit_price': Decimal('15.00'), 'stock_quantity': 30},
    {'name': 'Mini Pocket Notebook', 'sku': 'SKU065', 'category': 'Notebook', 'unit_price': Decimal('1.50'), 'stock_quantity': 200},
    {'name': 'Brown Envelope Extra Large', 'sku': 'SKU066', 'category': 'Office Supplies', 'unit_price': Decimal('1.20'), 'stock_quantity': 300},
    {'name': 'Security Envelope', 'sku': 'SKU067', 'category': 'Office Supplies', 'unit_price': Decimal('0.90'), 'stock_quantity': 320},
    {'name': 'Bubble Mailer Small', 'sku': 'SKU068', 'category': 'Packaging', 'unit_price': Decimal('0.70'), 'stock_quantity': 500},
    {'name': 'Bubble Mailer Medium', 'sku': 'SKU069', 'category': 'Packaging', 'unit_price': Decimal('0.90'), 'stock_quantity': 450},
    {'name': 'Bubble Mailer Large', 'sku': 'SKU070', 'category': 'Packaging', 'unit_price': Decimal('1.20'), 'stock_quantity': 400},
    {'name': 'Gift Wrapping Paper Roll', 'sku': 'SKU071', 'category': 'Packaging', 'unit_price': Decimal('3.00'), 'stock_quantity': 250},
    {'name': 'Wrapping Paper Sheet', 'sku': 'SKU072', 'category': 'Packaging', 'unit_price': Decimal('1.00'), 'stock_quantity': 300},
    {'name': 'Paper Cup Small', 'sku': 'SKU073', 'category': 'Other', 'unit_price': Decimal('0.10'), 'stock_quantity': 1000},
    {'name': 'Paper Cup Medium', 'sku': 'SKU074', 'category': 'Other', 'unit_price': Decimal('0.15'), 'stock_quantity': 900},
    {'name': 'Paper Cup Large', 'sku': 'SKU075', 'category': 'Other', 'unit_price': Decimal('0.20'), 'stock_quantity': 850},
    {'name': 'Paper Plate Small', 'sku': 'SKU076', 'category': 'Other', 'unit_price': Decimal('0.25'), 'stock_quantity': 800},
    {'name': 'Paper Plate Large', 'sku': 'SKU077', 'category': 'Other', 'unit_price': Decimal('0.40'), 'stock_quantity': 700},
    {'name': 'Premium Ledger Book', 'sku': 'SKU078', 'category': 'Notebook', 'unit_price': Decimal('12.00'), 'stock_quantity': 40},
    {'name': 'Accounting Register Large', 'sku': 'SKU079', 'category': 'Notebook', 'unit_price': Decimal('8.00'), 'stock_quantity': 75},
    {'name': 'Thermal POS Roll Premium', 'sku': 'SKU080', 'category': 'Office Supplies', 'unit_price': Decimal('3.00'), 'stock_quantity': 300},
    {'name': 'Plotter Paper Roll', 'sku': 'SKU081', 'category': 'Copy Paper', 'unit_price': Decimal('25.00'), 'stock_quantity': 20},
    {'name': 'Blueprint Paper A2', 'sku': 'SKU082', 'category': 'Copy Paper', 'unit_price': Decimal('5.00'), 'stock_quantity': 100},
    {'name': 'Blueprint Paper A1', 'sku': 'SKU083', 'category': 'Copy Paper', 'unit_price': Decimal('8.00'), 'stock_quantity': 60},
    {'name': 'Tracing Paper A4', 'sku': 'SKU084', 'category': 'Copy Paper', 'unit_price': Decimal('4.00'), 'stock_quantity': 120},
    {'name': 'Tracing Paper A3', 'sku': 'SKU085', 'category': 'Copy Paper', 'unit_price': Decimal('6.00'), 'stock_quantity': 90},
    {'name': 'Lamination Pouch A4', 'sku': 'SKU086', 'category': 'Office Supplies', 'unit_price': Decimal('0.50'), 'stock_quantity': 600},
    {'name': 'Lamination Pouch A3', 'sku': 'SKU087', 'category': 'Office Supplies', 'unit_price': Decimal('0.80'), 'stock_quantity': 500},
    {'name': 'Shredded Paper Packaging', 'sku': 'SKU088', 'category': 'Packaging', 'unit_price': Decimal('2.00'), 'stock_quantity': 150},
    {'name': 'Custom Printed Paper Bag', 'sku': 'SKU089', 'category': 'Packaging', 'unit_price': Decimal('1.50'), 'stock_quantity': 200},
    {'name': 'Food Wrapping Paper', 'sku': 'SKU090', 'category': 'Packaging', 'unit_price': Decimal('0.70'), 'stock_quantity': 350},
    {'name': 'Greaseproof Paper Sheet', 'sku': 'SKU091', 'category': 'Packaging', 'unit_price': Decimal('0.60'), 'stock_quantity': 400},
    {'name': 'Butter Paper Roll', 'sku': 'SKU092', 'category': 'Packaging', 'unit_price': Decimal('5.00'), 'stock_quantity': 70},
    {'name': 'Magazine Paper Glossy', 'sku': 'SKU093', 'category': 'Photo Paper', 'unit_price': Decimal('9.50'), 'stock_quantity': 80},
    {'name': 'Art Paper 150 GSM', 'sku': 'SKU094', 'category': 'Photo Paper', 'unit_price': Decimal('11.00'), 'stock_quantity': 60},
    {'name': 'Art Paper 200 GSM', 'sku': 'SKU095', 'category': 'Photo Paper', 'unit_price': Decimal('14.00'), 'stock_quantity': 50},
    {'name': 'Poster Paper A2', 'sku': 'SKU096', 'category': 'Copy Paper', 'unit_price': Decimal('4.50'), 'stock_quantity': 110},
    {'name': 'Poster Paper A1', 'sku': 'SKU097', 'category': 'Copy Paper', 'unit_price': Decimal('7.00'), 'stock_quantity': 90},
    {'name': 'Index Card Small', 'sku': 'SKU098', 'category': 'Office Supplies', 'unit_price': Decimal('1.00'), 'stock_quantity': 500},
    {'name': 'Index Card Large', 'sku': 'SKU099', 'category': 'Office Supplies', 'unit_price': Decimal('1.50'), 'stock_quantity': 450},
    {'name': 'Paper File Divider Set', 'sku': 'SKU100', 'category': 'Office Supplies', 'unit_price': Decimal('3.50'), 'stock_quantity': 220},
]

print("=" * 70)
print("SYNCING INITIAL PRODUCT DATA ONLY")
print("=" * 70)

target_skus = {item['sku'] for item in initial_products_data}

# Delete non-target products so frontend/API only show the initial list.
Product.objects.exclude(sku__in=target_skus).delete()

# Upsert target products to keep data consistent on re-runs.
for payload in initial_products_data:
    Product.objects.update_or_create(
        sku=payload['sku'],
        defaults={
            'name': payload['name'],
            'category': payload['category'],
            'unit_price': payload['unit_price'],
            'stock_quantity': payload['stock_quantity'],
        },
    )

print(f"Synced products count: {Product.objects.count()}")
print("Expected SKUs: SKU051 to SKU100")
print("=" * 70)
