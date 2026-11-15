from models import Customer, MenuItem, Order, Restaurant
from restaurant import RestaurantOrderManager


def main():
    restaurant = Restaurant("Example Restaurant")
    manager = RestaurantOrderManager(restaurant)

    burger = MenuItem(1, "Burger", 8.99)
    fries = MenuItem(2, "Fries", 3.49)
    drink = MenuItem(3, "Drink", 2.49)

    restaurant.add_menu_item(burger)
    restaurant.add_menu_item(fries)
    restaurant.add_menu_item(drink)

    customer = Customer(1, "John Smith", "555-1234")
    restaurant.add_customer(customer)

    order = Order(1001, customer)
    order.add_item(burger)
    order.add_item(fries)

    manager.submit_order(order)

    print("Restaurant Order Management System")
    print("---------------------------------")
    print(f"Submitted: {order}")
    print(f"Queue size: {len(manager.order_queue)}")

    processed = manager.process_next_order()
    print(f"Processed: {processed}")
    print(f"History size: {len(manager.order_history)}")


if __name__ == "__main__":
    main()
