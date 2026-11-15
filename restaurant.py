from models import Customer, MenuItem, Order, Restaurant
from queue import OrderQueue
from stack import OrderHistoryStack


class RestaurantOrderManager:
    """Coordinates restaurant orders using the Queue and Stack."""

    def __init__(self, restaurant: Restaurant):
        self.restaurant = restaurant
        self.order_queue = OrderQueue()
        self.order_history = OrderHistoryStack()

    def submit_order(self, order: Order):
        self.restaurant.add_order(order)
        self.order_queue.enqueue(order)

    def process_next_order(self):
        order = self.order_queue.dequeue()
        order.set_status("Completed")
        self.order_history.push(order)
        return order

    def undo_last_processed_order(self):
        if self.order_history.is_empty():
            raise IndexError("There are no processed orders to undo.")

        order = self.order_history.pop()
        order.set_status("Pending")
        self.order_queue.enqueue(order)
        return order

    def sort_orders_by_id(self):
        """Programmer-written insertion sort. Returns a new sorted list."""
        sorted_orders = self.restaurant.orders.copy()

        for i in range(1, len(sorted_orders)):
            key = sorted_orders[i]
            j = i - 1

            while j >= 0 and sorted_orders[j].order_id > key.order_id:
                sorted_orders[j + 1] = sorted_orders[j]
                j -= 1

            sorted_orders[j + 1] = key

        return sorted_orders
