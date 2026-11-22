# Restaurant Order Management System

Python Data Structures Final Project

## Sprint 1
- Customer, MenuItem, Order, Restaurant, and RestaurantOrderManager classes
- Custom linked-node FIFO queue (`OrderQueue`)
- Custom linked-node LIFO stack (`OrderHistoryStack`)
- Programmer-written insertion sort by order ID
- Unit tests for models and data structures

## Sprint 2
- Tkinter graphical interface with Menu, Customers, Create Order, and Order Display tabs
- Input validation for required text, numeric IDs, and nonnegative prices
- Order creation, item selection/removal, order totals, FIFO processing, and order display
- Validation and regression unit tests

## Requirements
Python 3.10 or newer is recommended. Tkinter is included with most standard Windows Python installations.

## Run the application
From this folder:

```bash
python main.py
```

## Run unit tests
```bash
python -m unittest discover -s tests -v
```

## Notes
The GUI currently stores data in memory. Closing the application clears the session. Saving data between sessions can be considered as a future enhancement if required.
