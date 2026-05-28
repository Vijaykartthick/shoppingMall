import sqlite3

# Database connection
conn = sqlite3.connect("mall.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER
)
""")

conn.commit()

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    quantity = int(input("Enter quantity: "))

    cursor.execute("""
    INSERT INTO products (name, price, quantity)
    VALUES (?, ?, ?)
    """, (name, price, quantity))

    conn.commit()
    print("Product added successfully!")


def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n--- Product List ---")

    if len(products) == 0:
        print("No products found!")

    else:
        for product in products:
            print(f"ID: {product[0]}")
            print(f"Name: {product[1]}")
            print(f"Price: ₹{product[2]}")
            print(f"Quantity: {product[3]}")
            print("----------------------")


def buy_product():
    product_id = int(input("Enter Product ID: "))
    buy_qty = int(input("Enter quantity to buy: "))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        available_qty = product[3]

        if buy_qty <= available_qty:
            total = buy_qty * product[2]
            new_qty = available_qty - buy_qty

            cursor.execute("""
            UPDATE products
            SET quantity=?
            WHERE id=?
            """, (new_qty, product_id))

            conn.commit()

            print("\n----- BILL -----")
            print(f"Product: {product[1]}")
            print(f"Price: ₹{product[2]}")
            print(f"Quantity: {buy_qty}")
            print(f"Total Bill: ₹{total}")
            print("----------------")

        else:
            print("Not enough stock available!")

    else:
        print("Product not found!")

def delete_product():
    product_id = int(input("Enter Product ID to delete: "))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    if product:
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        print("Product deleted successfully!")

    else:
        print("Product not found!")


while True:
    print("\n===== SHOPPING MALL APP =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Buy Product")
    print("4. Delete Product")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        view_products()

    elif choice == "3":
        buy_product()

    elif choice == "4":
        delete_product()

    elif choice == "5":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")
conn.close()