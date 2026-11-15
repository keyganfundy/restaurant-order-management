class _StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class OrderHistoryStack:
    """LIFO stack implemented with linked nodes."""

    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, order):
        node = _StackNode(order)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")

        order = self._top.value
        self._top = self._top.next
        self._size -= 1
        return order

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._top.value

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size

    def __len__(self):
        return self._size
