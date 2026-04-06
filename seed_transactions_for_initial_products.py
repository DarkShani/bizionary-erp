import random
import sqlite3
from datetime import datetime, timedelta


def main():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    product_rows = cur.execute(
        "SELECT id, sku, unit_price FROM products WHERE sku >= 'SKU051' AND sku <= 'SKU100' ORDER BY sku"
    ).fetchall()
    if not product_rows:
        raise RuntimeError('No target products found (SKU051-SKU100).')

    now = datetime.now()
    suppliers = ['Global Supplies', 'Tech Wholesale', 'Office Depot', 'Bulk Vendors']
    customers = ['Tech Solutions', 'Global Enterprises', 'XYZ Industries', 'Business Center', 'Smart Retail']

    # Seed Sales
    for i in range(60):
        p = random.choice(product_rows)
        qty = random.randint(1, 20)
        unit_price = float(p['unit_price'])
        total_price = round(unit_price * qty, 2)
        sale_date = (now - timedelta(days=random.randint(0, 120))).date().isoformat()
        stamp = (now - timedelta(days=random.randint(0, 120))).strftime('%Y-%m-%d %H:%M:%S')

        cur.execute(
            """
            INSERT INTO sales (
                quantity_sold, unit_price, total_price, payment_method,
                created_at, updated_at, product_id, customer_id,
                discount, invoice_number, notes, payment_status, sale_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                qty,
                unit_price,
                total_price,
                'CASH',
                stamp,
                stamp,
                p['id'],
                None,
                0.0,
                f'SINV-{now.year}-{1000 + i}',
                f'Seeded sale for {p["sku"]}',
                'PAID',
                sale_date,
            ),
        )

    # Seed Purchases
    for i in range(35):
        p = random.choice(product_rows)
        qty = random.randint(5, 40)
        unit_cost = round(float(p['unit_price']) * random.uniform(0.55, 0.85), 2)
        total_cost = round(unit_cost * qty, 2)
        purchase_date = (now - timedelta(days=random.randint(0, 120))).date().isoformat()
        stamp = (now - timedelta(days=random.randint(0, 120))).strftime('%Y-%m-%d %H:%M:%S')

        cur.execute(
            """
            INSERT INTO purchases (
                supplier_name, quantity_purchased, unit_cost, total_cost,
                purchase_date, payment_status, notes, created_at, updated_at, product_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                random.choice(suppliers),
                qty,
                unit_cost,
                total_cost,
                purchase_date,
                'PAID',
                f'Seeded purchase for {p["sku"]}',
                stamp,
                stamp,
                p['id'],
            ),
        )

    # Seed Invoices
    statuses = ['PAID', 'UNPAID', 'PARTIALLY_PAID', 'OVERDUE']
    for i in range(20):
        subtotal = round(random.uniform(4000, 70000), 2)
        tax = round(subtotal * 0.1, 2)
        discount = round(subtotal * random.uniform(0.0, 0.08), 2)
        total = round(subtotal + tax - discount, 2)
        status = random.choice(statuses)

        if status == 'PAID':
            amount_paid = total
        elif status == 'PARTIALLY_PAID':
            amount_paid = round(total * random.uniform(0.25, 0.75), 2)
        else:
            amount_paid = 0.0

        invoice_date = (now - timedelta(days=random.randint(0, 90))).date().isoformat()
        due_date = (now + timedelta(days=random.randint(3, 45))).date().isoformat()
        stamp = (now - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d %H:%M:%S')

        cur.execute(
            """
            INSERT INTO invoices (
                invoice_number, customer_name, customer_email, customer_phone,
                invoice_date, due_date, subtotal, tax_amount, discount_amount,
                total_amount, amount_paid, status, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f'INV-{now.year}-{2000 + i}',
                random.choice(customers),
                f'customer{i}@example.com',
                '03001234567',
                invoice_date,
                due_date,
                subtotal,
                tax,
                discount,
                total,
                amount_paid,
                status,
                'Seeded invoice',
                stamp,
                stamp,
            ),
        )

    conn.commit()

    sales_count = cur.execute('SELECT COUNT(*) AS c FROM sales').fetchone()['c']
    purchases_count = cur.execute('SELECT COUNT(*) AS c FROM purchases').fetchone()['c']
    invoices_count = cur.execute('SELECT COUNT(*) AS c FROM invoices').fetchone()['c']

    print('Inserted seed transactions successfully.')
    print('sales_total=', sales_count)
    print('purchases_total=', purchases_count)
    print('invoices_total=', invoices_count)


if __name__ == '__main__':
    main()
