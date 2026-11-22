import unittest
from models import Customer, MenuItem, Order, Restaurant
from order_queue import OrderQueue
from stack import OrderHistoryStack
from restaurant import RestaurantOrderManager

def make_order(order_id):
    customer = Customer(order_id, f"Customer {order_id}")
    return Order(order_id, customer, [MenuItem(1, "Burger", 8.99)])

class TestQueue(unittest.TestCase):
    def test_fifo(self):
        queue = OrderQueue()
        first, second = make_order(1), make_order(2)
        queue.enqueue(first)
        queue.enqueue(second)
        self.assertIs(queue.dequeue(), first)
        self.assertIs(queue.dequeue(), second)

    def test_empty_dequeue_raises(self):
        with self.assertRaises(IndexError):
            OrderQueue().dequeue()

class TestStack(unittest.TestCase):
    def test_lifo(self):
        stack = OrderHistoryStack()
        first, second = make_order(1), make_order(2)
        stack.push(first)
        stack.push(second)
        self.assertIs(stack.pop(), second)
        self.assertIs(stack.pop(), first)

    def test_empty_pop_raises(self):
        with self.assertRaises(IndexError):
            OrderHistoryStack().pop()

class TestOrderManager(unittest.TestCase):
    def test_process_order(self):
        restaurant = Restaurant("Test")
        manager = RestaurantOrderManager(restaurant)
        order = make_order(1)
        manager.submit_order(order)
        self.assertIs(manager.process_next_order(), order)
        self.assertEqual(order.status, "Completed")

    def test_insertion_sort(self):
        restaurant = Restaurant("Test")
        manager = RestaurantOrderManager(restaurant)
        for order_id in (30, 10, 20):
            manager.submit_order(make_order(order_id))
        self.assertEqual([o.order_id for o in manager.sort_orders_by_id()], [10, 20, 30])

if __name__ == "__main__":
    unittest.main()
