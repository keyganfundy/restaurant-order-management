import unittest

from models import Customer, MenuItem, Order
from queue import OrderQueue
from stack import OrderHistoryStack
from restaurant import RestaurantOrderManager
from models import Restaurant


def make_order(order_id):
    customer = Customer(order_id, f"Customer {order_id}")
    order = Order(order_id, customer)
    order.add_item(MenuItem(1, "Burger", 8.99))
    return order


class TestQueue(unittest.TestCase):

    def test_enqueue_dequeue_is_fifo(self):
        queue = OrderQueue()
        first = make_order(1)
        second = make_order(2)

        queue.enqueue(first)
        queue.enqueue(second)

        self.assertIs(queue.dequeue(), first)
        self.assertIs(queue.dequeue(), second)

    def test_queue_peek(self):
        queue = OrderQueue()
        order = make_order(1)
        queue.enqueue(order)

        self.assertIs(queue.peek(), order)
        self.assertEqual(queue.size(), 1)

    def test_empty_queue(self):
        queue = OrderQueue()

        self.assertTrue(queue.is_empty())

        with self.assertRaises(IndexError):
            queue.dequeue()


class TestStack(unittest.TestCase):

    def test_push_pop_is_lifo(self):
        stack = OrderHistoryStack()
        first = make_order(1)
        second = make_order(2)

        stack.push(first)
        stack.push(second)

        self.assertIs(stack.pop(), second)
        self.assertIs(stack.pop(), first)

    def test_stack_peek(self):
        stack = OrderHistoryStack()
        order = make_order(1)
        stack.push(order)

        self.assertIs(stack.peek(), order)
        self.assertEqual(stack.size(), 1)

    def test_empty_stack(self):
        stack = OrderHistoryStack()

        self.assertTrue(stack.is_empty())

        with self.assertRaises(IndexError):
            stack.pop()


class TestRestaurantOrderManager(unittest.TestCase):

    def test_processing_moves_order_to_history(self):
        restaurant = Restaurant("Test Restaurant")
        manager = RestaurantOrderManager(restaurant)
        order = make_order(1)

        manager.submit_order(order)
        processed = manager.process_next_order()

        self.assertIs(processed, order)
        self.assertEqual(order.status, "Completed")
        self.assertTrue(manager.order_queue.is_empty())
        self.assertIs(manager.order_history.peek(), order)

    def test_insertion_sort_by_order_id(self):
        restaurant = Restaurant("Test Restaurant")
        manager = RestaurantOrderManager(restaurant)

        manager.submit_order(make_order(30))
        manager.submit_order(make_order(10))
        manager.submit_order(make_order(20))

        sorted_orders = manager.sort_orders_by_id()

        self.assertEqual(
            [order.order_id for order in sorted_orders],
            [10, 20, 30]
        )


if __name__ == "__main__":
    unittest.main()
