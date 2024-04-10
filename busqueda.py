from queue import PriorityQueue

class Frontier:
    def __init__(self):
        self.values = []

    def push(self, value):
        self.values.append(value)

    def has(self, value):
        return value in self.values

    def is_empty(self):
        return len(self.values) == 0

class Queue(Frontier):
    def pop(self):
        return self.values.pop(0)

class Stack(Frontier):
    def pop(self):
        return self.values.pop()



class State:
    def __init__(self, value):
        self.value = value
        self.visited = False
        self.actions = []
        self.parent = None
    
    def add_action(self, other_value):
        if not other_value in self.actions:
            self.actions.append(other_value)

    def mark_visited(self):
        self.visited = True

    def mark_unvisited(self):
        self.visited = False

    def set_parent(self, parent):
        self.parent = parent

    def __lt__(self, other):
        return self.value <= other.value

    def __str__(self):
        return f"{self.value}, visited:{self.visited} -> {self.actions}"


class StateSpace():
    def __init__(self):
        self.states = {}

    def add_state(self, state):
        self.states[state.value] = state

    def get_state(self, value):
        if type(value) == tuple:
            return self.states[value[0]]
        return self.states[value]

    def add_edge(self, value1, value2):
        self.states[value1].add_action(value2)

    def add_weighted_edge(self, value1, value2, weight):
        self.states[value1].add_action((value2, weight))

    def reset_visits(self):
        for state in self.states.values():
            state.mark_unvisited()


class Searcher:
    def __init__(self, space):
        self.space = space

    def breadth_first(self, initial_value, end_value):
        return self.search(initial_value, end_value, Queue())

    def depth_first(self, initial_value, end_value):
        return self.search(initial_value, end_value, Stack())
    
    def uniform_cost(self, initial_value, end_value):
        return self.weighted_search(initial_value, end_value, PriorityQueue())

    def weighted_search(self, initial_value, end_value, frontier):
        initial_state = self.space.get_state(initial_value)
        frontier.put((0, initial_state))
        lowest_costs = {initial_state: 0}

        while not frontier.empty():
            current_cost, current_state = frontier.get()
            print(current_state.value, current_cost)
            # current_state.mark_visited()

            if current_state.value == end_value:
                print("Found", current_state.value, current_cost)
                return (self.build_solution_path(current_state), current_cost)

            for action in current_state.actions:
                next_state = self.space.get_state(action[0])
                new_cost = current_cost + action[1]

                if next_state not in lowest_costs or new_cost < lowest_costs[next_state]:
                    next_state.set_parent(current_state)
                    lowest_costs[next_state] = new_cost
                    print("Expanding:", next_state.value, new_cost)
                    frontier.put((new_cost, next_state))
        return []

    def search(self, initial_value, end_value, frontier):
        initial_state = self.space.get_state(initial_value)
        frontier.push(initial_state)

        while frontier:
            current_state = frontier.pop()
            current_state.mark_visited()

            if current_state.value == end_value:
                return self.build_solution_path(current_state)

            for action in current_state.actions:
                next_state = self.space.get_state(action)
                if not next_state.visited and not frontier.has(next_state):
                    next_state.set_parent(current_state)
                    frontier.push(next_state)
        return []

    def build_solution_path(self, state):
        path = []
        while state:
            path.append(state.value)
            state = state.parent
        return list(reversed(path))


if __name__ == "__main__":
    # space_dict = {
    #     'A': ['B', 'C'],
    #     'B': ['D', 'E'],
    #     'C': ['F'],
    #     'D': [],
    #     'E': [],
    #     'F': []
    # }
    # space_dict = {
    #     '0': ['1', '3'],
    #     '1': ['0', '2', '3', '5'],
    #     '2': ['1', '3', '5', '4'],
    #     '3': ['0', '1', '2', '4'],
    #     '4': ['2', '3', '6'],
    #     '5': ['1', '2'],
    #     '6': ['1', '4'],
    # }
    space_dict = {
        'A': [('B', 4), ('C', 5)],
        'B': [('A', 4), ('C', 11), ('D', 9), ('E', 7)],
        'C': [('A', 5), ('B', 11), ('E', 3)],
        'D': [('B', 9), ('E', 13), ('F', 2)],
        'E': [('B', 7), ('C', 3), ('D', 13), ('F', 6)],
        'F': [('D', 2), ('E', 6)],
    }
    state_values = space_dict.keys()

    space  = StateSpace()

    for value in state_values:
        space.add_state(State(value))

    for state, actions in space_dict.items():
        for action in actions:
            if type(action) == tuple:
                space.add_weighted_edge(state, action[0], action[1])
            else:
                space.add_edge(state, action)

    initial_value = 'A'
    end_value = 'F'

    searcher = Searcher(space)

    # print("Buscando en Profundidad")
    # print(searcher.depth_first('initial_value', 'end_value'))

    # space.reset_visits()

    # print("Buscando en amplitud")
    # print(searcher.breadth_first('initial_value', 'end_value'))

    # space.reset_visits()

    print("Buscando en costo uniforme")
    print(searcher.uniform_cost(initial_value, end_value))
