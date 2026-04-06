import ast
import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def load_initial_products_from_file(file_path: str):
    source = Path(file_path).read_text(encoding="utf-8")
    module = ast.parse(source)

    initial_node = None
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "initial_products_data":
                    initial_node = node.value
                    break
        if initial_node is not None:
            break

    if initial_node is None:
        raise RuntimeError("initial_products_data not found in insert_products.py")

    expr = ast.Expression(body=initial_node)
    return eval(compile(expr, filename="<ast>", mode="eval"), {"Decimal": Decimal})


def main():
    initial_products_data = load_initial_products_from_file("insert_products.py")
    keep_skus = [p["sku"] for p in initial_products_data]
    keep_set = set(keep_skus)

    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = [
        row["name"]
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    ]

    # Find tables that reference products via FK
    product_fk_refs = []
    for table in tables:
        try:
            fks = cur.execute(f"PRAGMA foreign_key_list('{table}')").fetchall()
        except sqlite3.OperationalError:
            continue

        for fk in fks:
            if fk["table"] == "products":
                product_fk_refs.append((table, fk["from"]))

    placeholders = ",".join(["?"] * len(keep_skus))

    # Remove rows from child tables for products that are not in target SKU list
    for table, from_col in product_fk_refs:
        delete_child_sql = (
            f"DELETE FROM {table} "
            f"WHERE {from_col} IN (SELECT id FROM products WHERE sku NOT IN ({placeholders}))"
        )
        cur.execute(delete_child_sql, keep_skus)

    # Remove out-of-scope products
    cur.execute(f"DELETE FROM products WHERE sku NOT IN ({placeholders})", keep_skus)

    # Upsert target products exactly from list
    product_cols = {
        row["name"] for row in cur.execute("PRAGMA table_info('products')").fetchall()
    }
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in initial_products_data:
        existing = cur.execute(
            "SELECT id FROM products WHERE sku = ?", (item["sku"],)
        ).fetchone()

        if existing:
            updates = []
            values = []
            for col, val in [
                ("name", item["name"]),
                ("category", item["category"]),
                ("unit_price", str(item["unit_price"])),
                ("stock_quantity", int(item["stock_quantity"])),
                ("reorder_level", 20),
                ("updated_at", now),
            ]:
                if col in product_cols:
                    updates.append(f"{col} = ?")
                    values.append(val)

            values.append(item["sku"])
            cur.execute(f"UPDATE products SET {', '.join(updates)} WHERE sku = ?", values)
        else:
            insert_cols = []
            insert_vals = []
            for col, val in [
                ("name", item["name"]),
                ("sku", item["sku"]),
                ("description", None),
                ("category", item["category"]),
                ("unit_price", str(item["unit_price"])),
                ("stock_quantity", int(item["stock_quantity"])),
                ("reorder_level", 20),
                ("created_at", now),
                ("updated_at", now),
            ]:
                if col in product_cols:
                    insert_cols.append(col)
                    insert_vals.append(val)

            insert_placeholders = ",".join(["?"] * len(insert_cols))
            cur.execute(
                f"INSERT INTO products ({', '.join(insert_cols)}) VALUES ({insert_placeholders})",
                insert_vals,
            )

    conn.commit()

    product_count = cur.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
    all_skus = [
        row["sku"] for row in cur.execute("SELECT sku FROM products ORDER BY sku").fetchall()
    ]

    sales_count = 0
    purchases_count = 0
    if "sales" in tables:
        sales_count = cur.execute("SELECT COUNT(*) AS c FROM sales").fetchone()["c"]
    if "purchases" in tables:
        purchases_count = cur.execute("SELECT COUNT(*) AS c FROM purchases").fetchone()["c"]

    print("products_total=", product_count)
    print("sales_total=", sales_count)
    print("purchases_total=", purchases_count)
    print("first_skus=", all_skus[:5])
    print("last_skus=", all_skus[-5:])
    print("all_target_only=", set(all_skus) == keep_set)
    print("fk_product_tables=", product_fk_refs)


if __name__ == "__main__":
    main()
