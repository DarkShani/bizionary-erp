import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cols = [row[1] for row in cur.execute("PRAGMA table_info(sales)").fetchall()]

if 'customer_name' not in cols:
    cur.execute("ALTER TABLE sales ADD COLUMN customer_name varchar(255)")
    cur.execute("UPDATE sales SET customer_name='Walk-in Customer' WHERE customer_name IS NULL OR customer_name=''")
    conn.commit()

cols_after = [row[1] for row in cur.execute("PRAGMA table_info(sales)").fetchall()]
print('customer_name_added=', 'customer_name' in cols_after)
