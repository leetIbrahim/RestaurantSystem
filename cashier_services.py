def log_transaction(amount, payment_method):
    """Log each transaction to the transactions.txt file."""
    try:
        with open('data/transactions.txt', 'a') as file:
            file.write(f"{amount:.2f},{payment_method}\n")
    except Exception as e:
        print(f"Error logging transaction: {e}")

def log_sale(item, quantity, amount):
    """Log each item sold to the daily_sales.txt file with correct quantity and total amount."""
    try:
        with open('data/daily_sales.txt', 'a') as file:
            file.write(f"{item},{quantity},{amount * quantity}\n")  # Ensure amount reflects total sale
    except Exception as e:
        print(f"Error logging sale: {e}")


def read_order_details(order_id, takeaway):
    """Fetch order details based on order ID."""
    orders = []
    total = 0
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                # Ensure we're matching the order ID and expecting 7 parts per line
                if parts[0] == order_id and len(parts) == 7:
                    _, _, _, _, item, quantity, price = parts
                    quantity = int(quantity)
                    price = float(price)
                    total_price = quantity * price
                    orders.append(f"{item} x {quantity}: {total_price:.2f}")
                    total += total_price
    except FileNotFoundError:
        print("Orders file not found. Please ensure the 'data/orders.txt' file exists.")
    # Adjust for takeaway charge
    if takeaway:
        total += len(orders)  # Assuming RM1 for each item if takeaway
    return orders, total


def generate_cash_bill():
    """Generate a bill for an order."""
    order_id = input("Enter the order ID to generate bill: ")
    takeaway = input("Is this order takeaway? (yes/no): ").lower().startswith('y')
    orders, total = read_order_details(order_id, takeaway)
    
    if not orders:
        print("Order not found.")
        return
    
    service_charge = total * 0.10
    gst = total * 0.06
    final_total = total + service_charge + gst
    if takeaway:
        takeaway_charge = len(orders)  # RM1 for each item if takeaway
        final_total += takeaway_charge
    print("\n--- Bill Summary ---")
    print("\n".join(orders))
    print(f"Subtotal: {total:.2f}")
    if takeaway:
        print(f"Takeaway Packing Charge: {takeaway_charge:.2f}")
    print(f"Service Charge (10%): {service_charge:.2f}")
    print(f"Government Service Tax (6%): {gst:.2f}")
    print(f"Total: {final_total:.2f}")
    
    payment_method = input("Enter payment method (cash, e-wallet, debit, credit card): ")
    log_transaction(final_total, payment_method)
    # Log each sale
    for order_line in orders:
        item, price = order_line.split(': ')
        log_sale(item, 1, float(price))  # Log the sale with quantity as 1 for simplicity
    print(f"Payment of {final_total:.2f} received via {payment_method}. Thank you!")

def end_of_day_processing():
    """Process transactions at the end of the day."""
    print("End of Day Summary:")
    total_cash = total_card = total_ewallet = 0.0
    try:
        with open('data/transactions.txt', 'r') as file:
            for line in file:
                amount, method = line.strip().split(',')
                amount = float(amount)
                if method == "cash":
                    total_cash += amount
                elif method in ["debit", "credit card"]:
                    total_card += amount
                elif method == "e-wallet":
                    total_ewallet += amount
    except FileNotFoundError:
        print("Transactions file not found. No transactions for today.")
        return
    
    print(f"Total Cash Received: {total_cash:.2f}")
    print(f"Total Card Payments: {total_card:.2f}")
    print(f"Total E-Wallet Payments: {total_ewallet:.2f}")


def daily_sales_analytics():
    sales_data = {}
    try:
        with open('data/daily_sales.txt', 'r') as file:
            for line in file:
                item, quantity, amount = line.strip().split(',')
                if item in sales_data:
                    sales_data[item]['quantity'] += int(quantity)
                    sales_data[item]['amount'] += float(amount)
                else:
                    sales_data[item] = {'quantity': int(quantity), 'amount': float(amount)}
    except FileNotFoundError:
        print("Daily sales file not found. Please ensure the 'data/daily_sales.txt' file exists.")
        return

    if not sales_data:
        print("No sales data available for today.")
        return

    total_sales_amount = sum(item['amount'] for item in sales_data.values())
    total_sales_quantity = sum(item['quantity'] for item in sales_data.values())

    top_selling_item = max(sales_data.items(), key=lambda x: x[1]['quantity'])
    least_selling_item = min(sales_data.items(), key=lambda x: x[1]['quantity'])

    print("\n--- Daily Sales Analytics ---")
    print(f"Total Sales Amount: {total_sales_amount:.2f}")
    print(f"Total Number of Sales: {total_sales_quantity}")
    print(f"Top Selling Food Item: {top_selling_item[0]} (Quantity Sold: {top_selling_item[1]['quantity']})")
    print(f"Least Selling Food Item: {least_selling_item[0]} (Quantity Sold: {least_selling_item[1]['quantity']})")


def cashier_interface():
    while True:
        print("\n╔═══════════════════════════════════╗")
        print("║       Cashier Interface           ║")
        print("╠═══════════════════════════════════╣")
        print("║ 1. Generate Cash Bill             ║")
        print("║ 2. End of Day Processing          ║")
        print("║ 3. Daily Sales Analytics          ║")
        print("║ 4. Exit                           ║")
        print("╚═══════════════════════════════════╝")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            generate_cash_bill()
        elif choice == '2':
            end_of_day_processing()  # Implement this based on your system's needs
        elif choice == '3':
            daily_sales_analytics()  # Implement this based on your system's needs
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    cashier_interface()