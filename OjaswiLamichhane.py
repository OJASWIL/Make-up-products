import os
from datetime import datetime

PRODUCTS_FILE = "products.txt"

# Load products from file
def load_products():
    products = []
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 5:
                    name, brand, qty, cost, country = parts
                    products.append({
                        "name": name,
                        "brand": brand,
                        "qty": int(qty),
                        "cost": float(cost),
                        "country": country
                    })
    else:
        print("⚠️  Note: 'products.txt' not found.")
    return products

# Save products to file
def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        for p in products:
            file.write(f"{p['name']}, {p['brand']}, {p['qty']}, {p['cost']}, {p['country']}\n")

# Display product list
def show_products(products):
    if not products:
        print("\n⚠️  No products available (products.txt not found or empty).\n")
        return
    print("\nAvailable Products:")
    print("Name | Brand | Stock | Cost | Sell Price | Country")
    for p in products:
        sell_price = p['cost'] * 2
        print(f"{p['name']} | {p['brand']} | {p['qty']} | Rs.{p['cost']} | Rs.{sell_price} | {p['country']}")

# Unique filename generator
def generate_filename(prefix):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Sell products to customer
def sell_product(products):
    name = input("Enter customer name: ")
    while True:
        try:
            n = int(input("How many types of products? "))
            break
        except ValueError:
            print("Invalid number. Try again.")

    total = 0
    sold_items = []

    for _ in range(n):
        pname = input("Product name: ")
        while True:
            try:
                qty = int(input("Quantity to buy: "))
                break
            except ValueError:
                print("Please enter a valid number.")

        found = False
        for p in products:
            if p['name'].lower() == pname.lower():
                found = True
                free = qty // 3
                total_needed = qty + free
                if p['qty'] >= total_needed:
                    sell_price = p['cost'] * 2
                    amount = qty * sell_price
                    p['qty'] -= total_needed
                    sold_items.append((p['name'], p['brand'], qty, free, amount))
                    total += amount
                else:
                    print("Not enough stock!")
                break
        if not found:
            print("Product not found!")

    if sold_items:
        filename = generate_filename("invoice")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Customer: {name}\nDate: {datetime.now()}\n\n")
            for item in sold_items:
                f.write(f"Product: {item[0]}, Brand: {item[1]}, Qty: {item[2]}, Free: {item[3]}, Subtotal: Rs.{item[4]}\n")
            f.write(f"\nTotal: Rs.{total}\n")
        print(f"Invoice saved as {filename}")
    save_products(products)

# Purchase products from vendor
def restock_products(products):
    vendor = input("Enter vendor name: ")
    while True:
        try:
            n = int(input("How many products to purchase? "))
            break
        except ValueError:
            print("Please enter a valid number.")

    restocked = []

    for _ in range(n):
        name = input("Product name: ")
        brand = input("Brand: ")

        while True:
            try:
                qty = int(input("Quantity: "))
                break
            except ValueError:
                print("Enter a valid quantity.")

        while True:
            try:
                cost = float(input("Cost Price: "))
                break
            except ValueError:
                print("Enter a valid cost.")

        country = input("Country: ")

        for p in products:
            if p['name'].lower() == name.lower():
                p['qty'] += qty
                p['cost'] = cost
                break
        else:
            products.append({
                "name": name,
                "brand": brand,
                "qty": qty,
                "cost": cost,
                "country": country
            })

        restocked.append((name, brand, qty, cost))

    filename = generate_filename("restock")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Vendor: {vendor}\nDate: {datetime.now()}\n\n")
        for item in restocked:
            total = item[2] * item[3]
            f.write(f"Product: {item[0]}, Brand: {item[1]}, Qty: {item[2]}, Cost: Rs.{item[3]}, Total: Rs.{total}\n")
    print(f"Purchase note saved as {filename}")
    save_products(products)

# Main loop
def main():
    products = load_products()

    while True:
        print("\n--- WeCare Product System ---")
        print("1. Show Products")
        print("2. Sell Products to Customer")
        print("3. Purchase Products from Vendor")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        if choice == "1":
            show_products(products)
        elif choice == "2":
            sell_product(products)
        elif choice == "3":
            restock_products(products)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
