from dataclasses import dataclass, field


@dataclass
class Customer:
    customer_id: int
    name: str
    phone: str = ""

    def __post_init__(self):
        if self.customer_id <= 0:
            raise ValueError("Customer ID must be greater than 0.")
        if not self.name.strip():
            raise ValueError("Customer name cannot be blank.")

    def __str__(self):
        return f"{self.customer_id}: {self.name}"


@dataclass
class MenuItem:
    item_id: int
    name: str
    price: float

    def __post_init__(self):
        if self.item_id <= 0:
            raise ValueError("Menu item ID must be greater than 0.")
        if not self.name.strip():
            raise ValueError("Menu item name cannot be blank.")
        if self.price < 0:
            raise ValueError("Menu item price cannot be negative.")

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


@dataclass
class Order:
    order_id: int
    customer: Customer
    items: list[MenuItem] = field(default_factory=list)
    status: str = "Pending"

    def __post_init__(self):
        if self.order_id <= 0:
            raise ValueError("Order ID must be greater than 0.")
        if self.status not in {"Pending", "Preparing", "Completed", "Cancelled"}:
            raise ValueError("Invalid order status.")

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def total(self) -> float:
        return sum(item.price for item in self.items)

    def set_status(self, status: str):
        valid_statuses = {"Pending", "Preparing", "Completed", "Cancelled"}
        if status not in valid_statuses:
            raise ValueError("Invalid order status.")
        self.status = status

    def __str__(self):
        return (
            f"Order #{self.order_id} | {self.customer.name} | "
            f"${self.total():.2f} | {self.status}"
        )


class Restaurant:
    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Restaurant name cannot be blank.")

        self.name = name
        self.menu: list[MenuItem] = []
        self.customers: list[Customer] = []
        self.orders: list[Order] = []

    def add_menu_item(self, item: MenuItem):
        if any(existing.item_id == item.item_id for existing in self.menu):
            raise ValueError("Menu item ID already exists.")
        self.menu.append(item)

    def add_customer(self, customer: Customer):
        if any(existing.customer_id == customer.customer_id for existing in self.customers):
            raise ValueError("Customer ID already exists.")
        self.customers.append(customer)

    def add_order(self, order: Order):
        if any(existing.order_id == order.order_id for existing in self.orders):
            raise ValueError("Order ID already exists.")
        self.orders.append(order)

    def find_customer(self, customer_id: int):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def find_order(self, order_id: int):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None
