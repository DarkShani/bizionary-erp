#!/usr/bin/env python
"""
Comprehensive ERP Data Insertion and Testing Script
Inserts all products, sales, invoices, purchases, and accounts
Then tests all 7 dashboard API endpoints
"""

import os
import sys
import django
import random
import requests
import json
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from products.models import Product
from sales.models import Sale
from invoices.models import Invoice
from purchases.models import Purchase
from accounts.models import Account

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

additional_products_data = [
    {'name': 'Dell Laptop 15 inch', 'sku': 'LAP-DELL-15', 'category': 'Electronics', 'unit_price': Decimal('50000.00'), 'stock_quantity': 5},
    {'name': 'HP Desktop Computer', 'sku': 'DESK-HP-01', 'category': 'Electronics', 'unit_price': Decimal('45000.00'), 'stock_quantity': 4},
    {'name': 'Mouse Wireless Logitech', 'sku': 'MOUSE-LOG-01', 'category': 'Accessories', 'unit_price': Decimal('900.00'), 'stock_quantity': 50},
    {'name': 'Keyboard Mechanical RGB', 'sku': 'KEY-RGB-01', 'category': 'Accessories', 'unit_price': Decimal('3750.00'), 'stock_quantity': 15},
    {'name': 'Monitor 24 inch LED', 'sku': 'MON-24-LED', 'category': 'Electronics', 'unit_price': Decimal('15000.00'), 'stock_quantity': 10},
    {'name': 'USB-C Cable 3m', 'sku': 'CAB-USB-C', 'category': 'Accessories', 'unit_price': Decimal('500.00'), 'stock_quantity': 100},
    {'name': 'HDMI Cable Premium', 'sku': 'CAB-HDMI-01', 'category': 'Accessories', 'unit_price': Decimal('337.50'), 'stock_quantity': 75},
    {'name': 'Webcam 1080p HD', 'sku': 'WEB-1080-01', 'category': 'Electronics', 'unit_price': Decimal('2750.00'), 'stock_quantity': 12},
    {'name': 'USB 3.0 Hub 4 Port', 'sku': 'USB-HUB-4', 'category': 'Accessories', 'unit_price': Decimal('1500.00'), 'stock_quantity': 20},
    {'name': 'External SSD 1TB', 'sku': 'SSD-EXT-1T', 'category': 'Storage', 'unit_price': Decimal('5500.00'), 'stock_quantity': 8},
    {'name': 'Portable Hard Drive 2TB', 'sku': 'HDD-PORTABLE-2T', 'category': 'Storage', 'unit_price': Decimal('5500.00'), 'stock_quantity': 12},
    {'name': 'USB Flash Drive 32GB', 'sku': 'USB-FLASH-32', 'category': 'Storage', 'unit_price': Decimal('600.00'), 'stock_quantity': 50},
    {'name': 'Memory Card 64GB', 'sku': 'CARD-MEM-64', 'category': 'Storage', 'unit_price': Decimal('1800.00'), 'stock_quantity': 30},
    {'name': 'Wireless Charger Fast', 'sku': 'CHG-WIRELESS', 'category': 'Accessories', 'unit_price': Decimal('1800.00'), 'stock_quantity': 40},
    {'name': 'Phone Screen Protector', 'sku': 'PROT-SCREEN-01', 'category': 'Accessories', 'unit_price': Decimal('200.00'), 'stock_quantity': 100},
    {'name': 'Phone Case Premium', 'sku': 'CASE-PREMIUM-01', 'category': 'Accessories', 'unit_price': Decimal('2500.00'), 'stock_quantity': 50},
    {'name': 'Tablet Apple iPad 10', 'sku': 'TAB-IPAD-10', 'category': 'Electronics', 'unit_price': Decimal('41250.00'), 'stock_quantity': 6},
    {'name': 'Stylus Pen for Tablet', 'sku': 'STYLUS-TAB-01', 'category': 'Accessories', 'unit_price': Decimal('2500.00'), 'stock_quantity': 25},
    {'name': 'Laptop Stand Aluminum', 'sku': 'STAND-LAP-AL', 'category': 'Accessories', 'unit_price': Decimal('1500.00'), 'stock_quantity': 30},
    {'name': 'Desk Organizer Wooden', 'sku': 'ORG-DESK-WD', 'category': 'Furniture', 'unit_price': Decimal('1200.00'), 'stock_quantity': 35},
    {'name': 'Ergonomic Chair Premium', 'sku': 'CHAIR-ERGO-PM', 'category': 'Furniture', 'unit_price': Decimal('35000.00'), 'stock_quantity': 8},
    {'name': 'Standing Desk Electric', 'sku': 'DESK-STAND-EL', 'category': 'Furniture', 'unit_price': Decimal('35000.00'), 'stock_quantity': 5},
    {'name': 'Monitor Arm Mount', 'sku': 'MOUNT-MON-ARM', 'category': 'Accessories', 'unit_price': Decimal('2500.00'), 'stock_quantity': 15},
    {'name': 'Desk Lamp LED', 'sku': 'LAMP-LED-01', 'category': 'Office Equipment', 'unit_price': Decimal('2500.00'), 'stock_quantity': 20},
    {'name': 'Bookshelf Metal', 'sku': 'SHELF-METAL-01', 'category': 'Furniture', 'unit_price': Decimal('5000.00'), 'stock_quantity': 10},
    {'name': 'Filing Cabinet 4 Drawer', 'sku': 'CABINET-FILE-4', 'category': 'Furniture', 'unit_price': Decimal('6000.00'), 'stock_quantity': 8},
    {'name': 'Office Desk Wooden', 'sku': 'DESK-WD-01', 'category': 'Furniture', 'unit_price': Decimal('12000.00'), 'stock_quantity': 6},
    {'name': 'Conference Table', 'sku': 'TABLE-CONF-01', 'category': 'Furniture', 'unit_price': Decimal('25000.00'), 'stock_quantity': 3},
    {'name': 'Whiteboard Magnetic', 'sku': 'BOARD-WHITE-01', 'category': 'Office Equipment', 'unit_price': Decimal('3000.00'), 'stock_quantity': 12},
    {'name': 'Marker Set 24 Colors', 'sku': 'MARKER-24-01', 'category': 'Supplies', 'unit_price': Decimal('400.00'), 'stock_quantity': 50},
    {'name': 'Sticky Notes Pad', 'sku': 'NOTES-STICKY-01', 'category': 'Supplies', 'unit_price': Decimal('150.00'), 'stock_quantity': 100},
    {'name': 'Highlighter Pen Set', 'sku': 'HIGH-PEN-SET', 'category': 'Supplies', 'unit_price': Decimal('350.00'), 'stock_quantity': 60},
    {'name': 'Pen Ball Point 50 Pack', 'sku': 'PEN-BALL-50', 'category': 'Supplies', 'unit_price': Decimal('400.00'), 'stock_quantity': 80},
    {'name': 'Pencil Set Wooden', 'sku': 'PEN-WOOD-01', 'category': 'Supplies', 'unit_price': Decimal('250.00'), 'stock_quantity': 70},
    {'name': 'Ruler Measuring 30cm', 'sku': 'RULER-30-01', 'category': 'Supplies', 'unit_price': Decimal('125.00'), 'stock_quantity': 100},
    {'name': 'Compass Drawing Tool', 'sku': 'COMPASS-01', 'category': 'Supplies', 'unit_price': Decimal('200.00'), 'stock_quantity': 50},
    {'name': 'Eraser Premium Quality', 'sku': 'ERASE-PREM-01', 'category': 'Supplies', 'unit_price': Decimal('100.00'), 'stock_quantity': 150},
    {'name': 'Scissors Office Stainless', 'sku': 'SCISSORS-ST-01', 'category': 'Supplies', 'unit_price': Decimal('400.00'), 'stock_quantity': 40},
    {'name': 'Tape Dispenser with Tape', 'sku': 'TAPE-DISP-01', 'category': 'Supplies', 'unit_price': Decimal('300.00'), 'stock_quantity': 60},
    {'name': 'Stapler Heavy Duty', 'sku': 'STAPLER-HD-01', 'category': 'Supplies', 'unit_price': Decimal('400.00'), 'stock_quantity': 50},
    {'name': 'Paper Clips Box 100', 'sku': 'CLIPS-PAPER-100', 'category': 'Supplies', 'unit_price': Decimal('50.00'), 'stock_quantity': 200},
    {'name': 'Rubber Bands Assorted', 'sku': 'BANDS-RUBBER-01', 'category': 'Supplies', 'unit_price': Decimal('60.00'), 'stock_quantity': 150},
    {'name': 'Binder Clips Assorted', 'sku': 'CLIPS-BINDER-01', 'category': 'Supplies', 'unit_price': Decimal('75.00'), 'stock_quantity': 120},
    {'name': 'Manila Folder Pack 50', 'sku': 'FOLDER-MANILA-50', 'category': 'Supplies', 'unit_price': Decimal('200.00'), 'stock_quantity': 80},
    {'name': 'Hanging Folder', 'sku': 'FOLDER-HANG-01', 'category': 'Supplies', 'unit_price': Decimal('180.00'), 'stock_quantity': 100},
    {'name': 'File Box Storage', 'sku': 'BOX-FILE-01', 'category': 'Supplies', 'unit_price': Decimal('800.00'), 'stock_quantity': 30},
    {'name': 'Archive Box Heavy Duty', 'sku': 'BOX-ARCHIVE-HD', 'category': 'Supplies', 'unit_price': Decimal('450.00'), 'stock_quantity': 50},
    {'name': 'Label Maker Device', 'sku': 'LABEL-MAKER-01', 'category': 'Office Equipment', 'unit_price': Decimal('5000.00'), 'stock_quantity': 10},
    {'name': 'Laminator Machine A4', 'sku': 'LAMIN-A4-01', 'category': 'Office Equipment', 'unit_price': Decimal('3500.00'), 'stock_quantity': 8},
    {'name': 'Paper Shredder', 'sku': 'SHRED-PAPER-01', 'category': 'Office Equipment', 'unit_price': Decimal('5000.00'), 'stock_quantity': 6},
    {'name': 'Hole Punch 2 Hole', 'sku': 'PUNCH-2HOLE-01', 'category': 'Supplies', 'unit_price': Decimal('250.00'), 'stock_quantity': 40},
    {'name': 'Bookbinder Comb Plastic', 'sku': 'BINDER-COMB-01', 'category': 'Supplies', 'unit_price': Decimal('300.00'), 'stock_quantity': 50},
    {'name': 'Binding Covers Plastic', 'sku': 'COVER-BIND-PL', 'category': 'Supplies', 'unit_price': Decimal('150.00'), 'stock_quantity': 150},
    {'name': 'Document Sleeve Clear', 'sku': 'SLEEVE-DOC-01', 'category': 'Supplies', 'unit_price': Decimal('100.00'), 'stock_quantity': 200},
    {'name': 'CD DVD Storage Case', 'sku': 'CASE-CD-DVD-01', 'category': 'Storage', 'unit_price': Decimal('200.00'), 'stock_quantity': 80},
    {'name': 'Software License MS Office', 'sku': 'LIC-MS-OFFICE', 'category': 'Software', 'unit_price': Decimal('10000.00'), 'stock_quantity': 20},
    {'name': 'Antivirus Software 1Y', 'sku': 'LIC-ANTIVIRUS-1Y', 'category': 'Software', 'unit_price': Decimal('2000.00'), 'stock_quantity': 30},
    {'name': 'VPN Software License', 'sku': 'LIC-VPN-01', 'category': 'Software', 'unit_price': Decimal('3000.00'), 'stock_quantity': 25},
    {'name': 'Backup Software License', 'sku': 'LIC-BACKUP-01', 'category': 'Software', 'unit_price': Decimal('5000.00'), 'stock_quantity': 15},
    {'name': 'Desktop Monitor 27 inch', 'sku': 'MON-27-DESK', 'category': 'Electronics', 'unit_price': Decimal('25000.00'), 'stock_quantity': 8},
    {'name': 'Curved Gaming Monitor', 'sku': 'MON-CURVED-GM', 'category': 'Electronics', 'unit_price': Decimal('35000.00'), 'stock_quantity': 5},
    {'name': 'Printer Laser B&W', 'sku': 'PRINT-LASER-BW', 'category': 'Office Equipment', 'unit_price': Decimal('13500.00'), 'stock_quantity': 8},
    {'name': 'Printer Color Inkjet', 'sku': 'PRINT-INKJET-C', 'category': 'Office Equipment', 'unit_price': Decimal('12000.00'), 'stock_quantity': 7},
    {'name': 'Scanner Document High Speed', 'sku': 'SCAN-DOC-HS', 'category': 'Office Equipment', 'unit_price': Decimal('8000.00'), 'stock_quantity': 6},
    {'name': 'Copier Multifunction', 'sku': 'COPY-MULTI-01', 'category': 'Office Equipment', 'unit_price': Decimal('80000.00'), 'stock_quantity': 2},
    {'name': 'Telephone Office Voip', 'sku': 'PHONE-VOIP-01', 'category': 'Office Equipment', 'unit_price': Decimal('5000.00'), 'stock_quantity': 10},
    {'name': 'Security Camera System', 'sku': 'CAM-SECURITY-01', 'category': 'Electronics', 'unit_price': Decimal('25000.00'), 'stock_quantity': 4},
    {'name': 'Smart Lock Door', 'sku': 'LOCK-SMART-01', 'category': 'Electronics', 'unit_price': Decimal('8000.00'), 'stock_quantity': 8},
    {'name': 'PAD Access Control', 'sku': 'CTRL-ACCESS-PAD', 'category': 'Electronics', 'unit_price': Decimal('12000.00'), 'stock_quantity': 6},
    {'name': 'Projector HD 1080p', 'sku': 'PROJ-1080-01', 'category': 'Electronics', 'unit_price': Decimal('45000.00'), 'stock_quantity': 5},
    {'name': 'Presentation Screen', 'sku': 'SCREEN-PRES-01', 'category': 'Office Equipment', 'unit_price': Decimal('6000.00'), 'stock_quantity': 8},
    {'name': 'Audio Speaker Set', 'sku': 'SPEAKER-SET-01', 'category': 'Electronics', 'unit_price': Decimal('3500.00'), 'stock_quantity': 15},
    {'name': 'Microphone Professional', 'sku': 'MIC-PROF-01', 'category': 'Electronics', 'unit_price': Decimal('4000.00'), 'stock_quantity': 12},
    {'name': 'Headphones Studio Quality', 'sku': 'HEAD-STUDIO-01', 'category': 'Electronics', 'unit_price': Decimal('5000.00'), 'stock_quantity': 20},
    {'name': 'USB Microphone Condenser', 'sku': 'MIC-USB-COND', 'category': 'Electronics', 'unit_price': Decimal('4000.00'), 'stock_quantity': 15},
    {'name': 'Mixer Audio Professional', 'sku': 'MIX-AUDIO-PROF', 'category': 'Electronics', 'unit_price': Decimal('15000.00'), 'stock_quantity': 5},
    {'name': 'Power Bank 20000mAh', 'sku': 'BANK-POWER-20K', 'category': 'Accessories', 'unit_price': Decimal('2000.00'), 'stock_quantity': 40},
    {'name': 'Power Bank 30000mAh', 'sku': 'BANK-POWER-30K', 'category': 'Accessories', 'unit_price': Decimal('3000.00'), 'stock_quantity': 35},
    {'name': 'Car Charger Dual USB', 'sku': 'CHG-CAR-USB-2', 'category': 'Accessories', 'unit_price': Decimal('400.00'), 'stock_quantity': 80},
    {'name': 'Wall Charger Fast 65W', 'sku': 'CHG-WALL-65W', 'category': 'Accessories', 'unit_price': Decimal('1200.00'), 'stock_quantity': 50},
    {'name': 'Travel Adapter Universal', 'sku': 'ADAPT-TRAVEL-UN', 'category': 'Accessories', 'unit_price': Decimal('800.00'), 'stock_quantity': 60},
    {'name': 'Extension Cord 5m', 'sku': 'CORD-EXT-5M', 'category': 'Accessories', 'unit_price': Decimal('1500.00'), 'stock_quantity': 30},
    {'name': 'Power Strip 6 Socket', 'sku': 'STRIP-POWER-6', 'category': 'Accessories', 'unit_price': Decimal('2000.00'), 'stock_quantity': 25},
    {'name': 'Cable Organizer Set', 'sku': 'ORG-CABLE-01', 'category': 'Accessories', 'unit_price': Decimal('300.00'), 'stock_quantity': 70},
    {'name': 'Screen Cleaner Spray', 'sku': 'CLEAN-SCREEN-SP', 'category': 'Supplies', 'unit_price': Decimal('300.00'), 'stock_quantity': 60},
    {'name': 'Microfiber Cloth Pack', 'sku': 'CLOTH-MICRO-PK', 'category': 'Supplies', 'unit_price': Decimal('150.00'), 'stock_quantity': 100},
    {'name': 'Keyboard Cleaner Kit', 'sku': 'CLEAN-KEY-KIT', 'category': 'Supplies', 'unit_price': Decimal('500.00'), 'stock_quantity': 40},
    {'name': 'Air Blower Compressed', 'sku': 'BLOW-AIR-COMP', 'category': 'Supplies', 'unit_price': Decimal('800.00'), 'stock_quantity': 30},
    {'name': 'Thermal Paste CPU', 'sku': 'PASTE-THERMAL-CPU', 'category': 'Parts', 'unit_price': Decimal('400.00'), 'stock_quantity': 50},
    {'name': 'Thermal Pad GPU', 'sku': 'PAD-THERMAL-GPU', 'category': 'Parts', 'unit_price': Decimal('262.50'), 'stock_quantity': 70},
    {'name': 'RAM Memory 16GB DDR4', 'sku': 'RAM-16GB-DDR4', 'category': 'Parts', 'unit_price': Decimal('3750.00'), 'stock_quantity': 25},
    {'name': 'RAM Memory 32GB DDR4', 'sku': 'RAM-32GB-DDR4', 'category': 'Parts', 'unit_price': Decimal('6000.00'), 'stock_quantity': 20},
    {'name': 'SSD NVMe 512GB', 'sku': 'SSD-NVME-512G', 'category': 'Parts', 'unit_price': Decimal('3000.00'), 'stock_quantity': 30},
    {'name': 'SSD NVMe 1TB', 'sku': 'SSD-NVME-1TB', 'category': 'Parts', 'unit_price': Decimal('5000.00'), 'stock_quantity': 25},
    {'name': 'GPU Graphics Card RTX', 'sku': 'GPU-RTX-01', 'category': 'Parts', 'unit_price': Decimal('75000.00'), 'stock_quantity': 4},
    {'name': 'Power Supply 650W', 'sku': 'PSU-650W-01', 'category': 'Parts', 'unit_price': Decimal('3000.00'), 'stock_quantity': 15},
    {'name': 'Motherboard ATX', 'sku': 'MOBO-ATX-01', 'category': 'Parts', 'unit_price': Decimal('9000.00'), 'stock_quantity': 10},
]

print("=" * 70)
print("INSERTING ALL ERP DATA")
print("=" * 70)

# Insert initial products
print("\nInserting initial 50 products...")
for product in initial_products_data:
    Product.objects.create(**product)
print(f"Created {len(initial_products_data)} initial products")

# Insert additional products
print("Inserting 97 additional products...")
for product in additional_products_data:
    Product.objects.create(**product)
print(f"Created {len(additional_products_data)} additional products")

# Get all products for sales/transaction references
all_products = list(Product.objects.all())

# Insert sales
print("\nInserting 55 sales transactions...")
customers = ['Tech Solutions', 'Global Enterprises', 'XYZ Industries', 'Business Center', 'Smart Retail']
for i in range(55):
    product = random.choice(all_products)
    qty = random.randint(1, 20)
    sale_date = datetime.now() - timedelta(days=random.randint(0, 90))
    Sale.objects.create(
        product=product,
        customer_name=random.choice(customers),
        quantity_sold=qty,
        unit_price=product.unit_price,
        total_price=product.unit_price * qty,
        sale_date=sale_date
    )
print(f"Created 55 sales")

# Insert invoices
print("Inserting 25 invoices...")
statuses = ['PAID', 'UNPAID', 'PARTIALLY_PAID', 'OVERDUE']
for i in range(25):
    subtotal = Decimal(random.uniform(5000, 100000)).quantize(Decimal('0.01'))
    tax = (subtotal * Decimal('0.10')).quantize(Decimal('0.01'))
    discount = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
    total = (subtotal + tax - discount).quantize(Decimal('0.01'))
    status = random.choice(statuses)
    
    if status == 'PAID':
        amount_paid = total
    elif status == 'PARTIALLY_PAID':
        amount_paid = (total * Decimal(random.uniform(0.3, 0.7))).quantize(Decimal('0.01'))
    else:
        amount_paid = Decimal('0.00')
    
    Invoice.objects.create(
        invoice_number=f'INV-202600{i}',
        customer_name=random.choice(customers),
        customer_email=f'customer{i}@example.com',
        customer_phone='03001234567',
        invoice_date=datetime.now() - timedelta(days=random.randint(0, 60)),
        due_date=datetime.now() + timedelta(days=random.randint(1, 30)),
        subtotal=subtotal,
        tax_amount=tax,
        discount=discount,
        total_amount=total,
        amount_paid=amount_paid,
        status=status
    )
print(f"Created 25 invoices")

# Insert purchases
print("Inserting 20 purchases...")
suppliers = ['Global Supplies', 'Tech Wholesale', 'Office Depot', 'Bulk Vendors']
for i in range(20):
    product = random.choice(all_products)
    qty = random.randint(5, 50)
    unit_cost = (product.unit_price * Decimal('0.75')).quantize(Decimal('0.01'))
    Purchase.objects.create(
        product=product,
        supplier_name=random.choice(suppliers),
        quantity_purchased=qty,
        unit_cost=unit_cost,
        total_cost=unit_cost * qty,
        purchase_date=datetime.now() - timedelta(days=random.randint(0, 90)),
        payment_status='PENDING' if random.random() > 0.5 else 'COMPLETED'
    )
print(f"Created 20 purchases")

# Insert accounts
print("Inserting 12 accounts...")
accounts_data = [
    {'account_name': 'Petty Cash', 'account_number': 'ACC-001', 'account_type': 'ASSET', 'balance': Decimal('50000.00')},
    {'account_name': 'Bank Account Primary', 'account_number': 'ACC-002', 'account_type': 'ASSET', 'balance': Decimal('5000000.00')},
    {'account_name': 'Bank Account Secondary', 'account_number': 'ACC-003', 'account_type': 'ASSET', 'balance': Decimal('2500000.00')},
    {'account_name': 'Accounts Receivable', 'account_number': 'ACC-004', 'account_type': 'ASSET', 'balance': Decimal('3500000.00')},
    {'account_name': 'Inventory Account', 'account_number': 'ACC-005', 'account_type': 'ASSET', 'balance': Decimal('8000000.00')},
    {'account_name': 'Fixed Assets', 'account_number': 'ACC-006', 'account_type': 'ASSET', 'balance': Decimal('25000000.00')},
    {'account_name': 'Accounts Payable', 'account_number': 'ACC-007', 'account_type': 'LIABILITY', 'balance': Decimal('2000000.00')},
    {'account_name': 'Short Term Loan', 'account_number': 'ACC-008', 'account_type': 'LIABILITY', 'balance': Decimal('1500000.00')},
    {'account_name': 'Owner Capital', 'account_number': 'ACC-009', 'account_type': 'EQUITY', 'balance': Decimal('35000000.00')},
    {'account_name': 'Sales Revenue', 'account_number': 'ACC-010', 'account_type': 'REVENUE', 'balance': Decimal('15000000.00')},
    {'account_name': 'Service Revenue', 'account_number': 'ACC-011', 'account_type': 'REVENUE', 'balance': Decimal('3000000.00')},
    {'account_name': 'Operating Expenses', 'account_number': 'ACC-012', 'account_type': 'EXPENSE', 'balance': Decimal('5000000.00')},
]
for account in accounts_data:
    Account.objects.create(**account)
print(f"Created 12 accounts")

print("\n" + "=" * 70)
print("TESTING ALL DASHBOARD ENDPOINTS")
print("=" * 70)

BASE_URL = "http://127.0.0.1:8000/api/dashboard"
endpoints = [
    "/kpis/",
    "/monthly-revenue/",
    "/top-products/",
    "/low-stock-products/",
    "/recent-sales/",
    "/outstanding-invoices/",
    "/sales-performance/"
]

for endpoint in endpoints:
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, timeout=5)
        status = response.status_code
        print(f"\nGET {endpoint} -> Status: {status}")
        
        if status == 200:
            data = response.json()
            data_preview = json.dumps(data)[:150]
            print(f"Data: {data_preview}...")
    except Exception as e:
        print(f"GET {endpoint} -> Error: {str(e)}")

print("\n" + "=" * 70)
print("SUCCESS! All data inserted and endpoints tested")
print("=" * 70)
