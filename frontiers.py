from queue import PriorityQueue as _PriorityQueue

class Frontier():
    def __init__(self):
        self.values = []

    def put(self, value):
        self.values.append(value)

    def has(self, value):
        return value in self.values

    def empty(self):
        return len(self.values) == 0

class Stack(Frontier):
    def get(self):
        return self.values.pop()

class Queue(Frontier):
    def get(self):
        return self.values.pop(0)

class PrioritizedQueue(_PriorityQueue, Frontier):
    def __init__(self):
        _PriorityQueue.__init__(self)
        Frontier.__init__(self)

    def put(self, value):
        # value = (item, priority)
        _PriorityQueue.put(self, (value[1], value[0]))

    def get(self):
        priority, state = _PriorityQueue.get(self)
        return state, priority