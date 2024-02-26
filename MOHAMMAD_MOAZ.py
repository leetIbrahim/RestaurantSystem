import time

def display_orders():
    orders = [] 
    print("Welcome to the Restaurant Order System!")
    print("Press '4' to quit.")
    print("Press '2' to refresh the order list.")
    print("Press '1' to add a new order.")
    print("Press '3' to delete an order.")
    print()

    while True:
        action = input("Please enter an action (1/2/3/4): ").lower()
        if action == '4':
            print("Exiting the order system.")
            break
        elif action == '2':
            print("Refreshing the order list...")
            print()
            display_orders()
        elif action == '1':
            order = input("Please enter the new order: ")
            orders.append(order)
            print("Order added successfully.")
            print()
        elif action == '3':
            order_number = int(input("Please enter the order number you want to delete: "))
            if 1 <= order_number <= len(orders):
                deleted_order = orders.pop(order_number - 1)
                print(f"Order {order_number} deleted successfully: {deleted_order}")
                print()
            else:
                print("Invalid order number. Please try again.")
                print()
        else:
            print("Invalid action. Please try again.")
            print()

def main():
    while True:
        display_orders()
        time.sleep(5)  # wait for 5 seconds before refreshing the list

if __name__ == "__main__":
    main()

    