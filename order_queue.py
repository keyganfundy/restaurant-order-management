class _QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class OrderQueue:
    """FIFO queue implemented with linked nodes."""
    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def enqueue(self, order):
        node = _QueueNode(order)
        if self._rear is None:
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        order = self._front.value
        self._front = self._front.next
        self._size -= 1
        if self._front is None:
            self._rear = None
        return order

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")
        return self._front.value

    def is_empty(self):
        return self._front is None

    def size(self):
        return self._size

    def __len__(self):
        return self._size
