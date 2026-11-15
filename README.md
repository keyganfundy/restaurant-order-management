# Restaurant Order Management System

Final Project - Data Structures

## Sprint 1

Sprint 1 defines the core classes, implements two data structures, and creates unit tests.

### Classes

- `Customer` - stores customer information.
- `MenuItem` - stores menu item information.
- `Order` - stores an order and calculates its total.
- `Restaurant` - stores menu items, customers, and orders.
- `RestaurantOrderManager` - coordinates order processing.

### Data Structures

- `OrderQueue` - FIFO queue implemented with linked nodes.
- `OrderHistoryStack` - LIFO stack implemented with linked nodes.

### Sorting

`RestaurantOrderManager.sort_orders_by_id()` contains a programmer-written insertion sort.

### Running the program

```text
python main.py
```

### Running unit tests

```text
python -m unittest discover -s tests -v
```

The GUI will be added during Sprint 2.
