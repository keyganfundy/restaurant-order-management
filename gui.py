import tkinter as tk
from tkinter import ttk, messagebox

from models import Customer, MenuItem, Order, Restaurant
from restaurant import RestaurantOrderManager
from validation import required_text, positive_integer, nonnegative_price

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.restaurant = Restaurant("Restaurant Order Manager")
        self.manager = RestaurantOrderManager(self.restaurant)
        self.next_customer_id = 1
        self.next_menu_id = 1
        self.next_order_id = 1001
        self.order_item_ids = []

        self.root.title("Restaurant Order Management System")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self._build_interface()
        self._load_sample_menu()
        self._refresh_all()

    def _build_interface(self):
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="Restaurant Order Management System",
                  font=("Segoe UI", 19, "bold")).pack(anchor="w")
        ttk.Label(header, text="Manage menu items, customers, and incoming orders.",
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.menu_tab = ttk.Frame(self.tabs, padding=12)
        self.customer_tab = ttk.Frame(self.tabs, padding=12)
        self.order_tab = ttk.Frame(self.tabs, padding=12)
        self.display_tab = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.menu_tab, text="Menu")
        self.tabs.add(self.customer_tab, text="Customers")
        self.tabs.add(self.order_tab, text="Create Order")
        self.tabs.add(self.display_tab, text="Order Display")

        self._build_menu_tab()
        self._build_customer_tab()
        self._build_order_tab()
        self._build_display_tab()

    def _build_menu_tab(self):
        form = ttk.LabelFrame(self.menu_tab, text="Add Menu Item", padding=10)
        form.pack(fill="x")
        self.menu_name = tk.StringVar()
        self.menu_price = tk.StringVar()
        ttk.Label(form, text="Item name").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.menu_name, width=28).grid(row=1, column=0, padx=(0, 10), sticky="ew")
        ttk.Label(form, text="Price ($)").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.menu_price, width=14).grid(row=1, column=1, padx=(0, 10), sticky="ew")
        ttk.Button(form, text="Add Menu Item", command=self.add_menu_item).grid(row=1, column=2)
        form.columnconfigure(0, weight=1)

        self.menu_tree = self._make_tree(self.menu_tab, ("id", "name", "price"),
                                         ("ID", "Item", "Price"), (70, 350, 120))

    def _build_customer_tab(self):
        form = ttk.LabelFrame(self.customer_tab, text="Add Customer", padding=10)
        form.pack(fill="x")
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        ttk.Label(form, text="Customer name").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.customer_name, width=30).grid(row=1, column=0, padx=(0, 10), sticky="ew")
        ttk.Label(form, text="Phone (optional)").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.customer_phone, width=22).grid(row=1, column=1, padx=(0, 10))
        ttk.Button(form, text="Add Customer", command=self.add_customer).grid(row=1, column=2)
        form.columnconfigure(0, weight=1)

        self.customer_tree = self._make_tree(self.customer_tab, ("id", "name", "phone"),
                                              ("Customer ID", "Name", "Phone"), (110, 350, 180))

    def _build_order_tab(self):
        customer_frame = ttk.LabelFrame(self.order_tab, text="Customer", padding=10)
        customer_frame.pack(fill="x")
        self.order_customer = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_frame, textvariable=self.order_customer,
                                            state="readonly", width=55)
        self.customer_combo.pack(side="left", fill="x", expand=True)

        item_frame = ttk.LabelFrame(self.order_tab, text="Add Items to Order", padding=10)
        item_frame.pack(fill="x", pady=10)
        self.order_menu_item = tk.StringVar()
        self.menu_combo = ttk.Combobox(item_frame, textvariable=self.order_menu_item,
                                       state="readonly", width=55)
        self.menu_combo.pack(side="left", fill="x", expand=True)
        ttk.Button(item_frame, text="Add Selected Item", command=self.add_item_to_order).pack(side="left", padx=(8, 0))

        selected_frame = ttk.LabelFrame(self.order_tab, text="Current Order", padding=10)
        selected_frame.pack(fill="both", expand=True)
        self.selected_list = tk.Listbox(selected_frame, height=8)
        self.selected_list.pack(fill="both", expand=True)
        self.order_total_label = ttk.Label(selected_frame, text="Total: $0.00",
                                           font=("Segoe UI", 12, "bold"))
        self.order_total_label.pack(anchor="e", pady=8)
        buttons = ttk.Frame(selected_frame)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Remove Selected Item", command=self.remove_selected_item).pack(side="left")
        ttk.Button(buttons, text="Submit Order", command=self.submit_order).pack(side="right")

    def _build_display_tab(self):
        toolbar = ttk.Frame(self.display_tab)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(toolbar, text="Process Next Order", command=self.process_next_order).pack(side="left")
        ttk.Button(toolbar, text="Refresh", command=self._refresh_all).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Sort by Order ID", command=self.sort_display).pack(side="left")
        ttk.Label(toolbar, text="Pending orders are processed FIFO.",
                  font=("Segoe UI", 9, "italic")).pack(side="right")

        self.orders_tree = self._make_tree(
            self.display_tab, ("id", "customer", "items", "total", "status"),
            ("Order ID", "Customer", "Items", "Total", "Status"),
            (90, 180, 300, 100, 120)
        )
        history_frame = ttk.LabelFrame(self.display_tab, text="Recently Completed (latest first)", padding=8)
        history_frame.pack(fill="x", pady=(10, 0))
        self.history_list = tk.Listbox(history_frame, height=5)
        self.history_list.pack(fill="x")

    def _make_tree(self, parent, columns, headings, widths):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=(12, 0))
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def _load_sample_menu(self):
        samples = [("Burger", 8.99), ("Fries", 3.49), ("Soft Drink", 2.49),
                   ("Salad", 6.99), ("Chicken Sandwich", 9.49)]
        for name, price in samples:
            item = MenuItem(self.next_menu_id, name, price)
            self.restaurant.add_menu_item(item)
            self.next_menu_id += 1

    def add_menu_item(self):
        try:
            name = required_text(self.menu_name.get(), "Item name")
            price = nonnegative_price(self.menu_price.get())
            item = MenuItem(self.next_menu_id, name, price)
            self.restaurant.add_menu_item(item)
            self.next_menu_id += 1
            self.menu_name.set("")
            self.menu_price.set("")
            self._refresh_all()
        except ValueError as error:
            messagebox.showerror("Invalid Menu Item", str(error), parent=self.root)

    def add_customer(self):
        try:
            name = required_text(self.customer_name.get(), "Customer name")
            phone = self.customer_phone.get().strip()
            customer = Customer(self.next_customer_id, name, phone)
            self.restaurant.add_customer(customer)
            self.next_customer_id += 1
            self.customer_name.set("")
            self.customer_phone.set("")
            self._refresh_all()
        except ValueError as error:
            messagebox.showerror("Invalid Customer", str(error), parent=self.root)

    def add_item_to_order(self):
        selected = self.menu_combo.current()
        if selected < 0 or selected >= len(self.restaurant.menu):
            messagebox.showwarning("Select an Item", "Choose a menu item first.", parent=self.root)
            return
        item = self.restaurant.menu[selected]
        self.order_item_ids.append(item.item_id)
        self.selected_list.insert("end", f"{item.name} - ${item.price:.2f}")
        self._update_order_total()

    def remove_selected_item(self):
        selection = self.selected_list.curselection()
        if not selection:
            messagebox.showwarning("Select an Item", "Choose an order item to remove.", parent=self.root)
            return
        index = selection[0]
        self.selected_list.delete(index)
        del self.order_item_ids[index]
        self._update_order_total()

    def _update_order_total(self):
        lookup = {item.item_id: item for item in self.restaurant.menu}
        total = sum(lookup[item_id].price for item_id in self.order_item_ids)
        self.order_total_label.config(text=f"Total: ${total:.2f}")

    def submit_order(self):
        customer_index = self.customer_combo.current()
        if customer_index < 0 or customer_index >= len(self.restaurant.customers):
            messagebox.showwarning("Select Customer", "Add and select a customer before submitting an order.", parent=self.root)
            return
        if not self.order_item_ids:
            messagebox.showwarning("Empty Order", "Add at least one menu item before submitting.", parent=self.root)
            return
        customer = self.restaurant.customers[customer_index]
        lookup = {item.item_id: item for item in self.restaurant.menu}
        order = Order(self.next_order_id, customer,
                      [lookup[item_id] for item_id in self.order_item_ids])
        try:
            self.manager.submit_order(order)
        except ValueError as error:
            messagebox.showerror("Could Not Submit Order", str(error), parent=self.root)
            return
        self.next_order_id += 1
        self.order_item_ids.clear()
        self.selected_list.delete(0, "end")
        self._update_order_total()
        self._refresh_all()
        messagebox.showinfo("Order Submitted", f"Order #{order.order_id} was added to the queue.", parent=self.root)
        self.tabs.select(self.display_tab)

    def process_next_order(self):
        try:
            order = self.manager.process_next_order()
            self._refresh_all()
            messagebox.showinfo("Order Processed", f"Order #{order.order_id} is completed.", parent=self.root)
        except IndexError as error:
            messagebox.showwarning("No Pending Orders", str(error), parent=self.root)

    def sort_display(self):
        self._populate_orders(self.manager.sort_orders_by_id())

    def _populate_orders(self, orders):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        for order in orders:
            item_names = ", ".join(item.name for item in order.items)
            self.orders_tree.insert("", "end", values=(
                order.order_id, order.customer.name, item_names,
                f"${order.total():.2f}", order.status
            ))

    def _refresh_all(self):
        self._replace_tree(self.menu_tree, [
            (item.item_id, item.name, f"${item.price:.2f}") for item in self.restaurant.menu
        ])
        self._replace_tree(self.customer_tree, [
            (customer.customer_id, customer.name, customer.phone) for customer in self.restaurant.customers
        ])
        self.customer_combo["values"] = [
            f"{customer.customer_id} - {customer.name}" for customer in self.restaurant.customers
        ]
        self.menu_combo["values"] = [
            f"{item.name} - ${item.price:.2f}" for item in self.restaurant.menu
        ]
        self._populate_orders(self.restaurant.orders)
        self.history_list.delete(0, "end")
        # The custom stack intentionally exposes only pop/peek, so do not bypass its implementation.
        # Display the most recently completed item; full history traversal can be added later if needed.
        if not self.manager.order_history.is_empty():
            order = self.manager.order_history.peek()
            self.history_list.insert("end", str(order))

    @staticmethod
    def _replace_tree(tree, rows):
        for row in tree.get_children():
            tree.delete(row)
        for values in rows:
            tree.insert("", "end", values=values)

def run_app():
    root = tk.Tk()
    RestaurantApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
