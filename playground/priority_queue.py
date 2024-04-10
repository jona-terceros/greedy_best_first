from queue import PriorityQueue

# Create an instance of PriorityQueue
pq = PriorityQueue()

# Add elements to the queue with their priorities
pq.put((3, 'Apple'))
pq.put((1, 'Banana'))
pq.put((2, 'Cherry'))

# Verify wether 'Plumb' is in the queue value
# print('Plumb' in [item for priority, item in pq.queue])
# print('Apple' in [item for priority, item in pq.queue])

# Get and remove the elements from the queue in priority order
while not pq.empty():
  priority, item = pq.get()
  print(f'Priority: {priority}, Item: {item}')

