# 0. Implementar UCS (Uniform Cost Search) ✅

# 1. Este archivo está quedando grandote, dividirlo en módulos.

# 2. Añadir argumentos para desde la linea de comandos
#    ej. python busqueda_en_clases2.py --initial=A --goal=F --debug=True

# 3. ¿Es posible quitar el código repetido en los métodos de busqueda? Intentar refactorizar.

from frontiers import Stack, Queue, PrioritizedQueue

class State:
    def __init__(self, value):
        self.value = value
        self.actions = []
        self.visited = False
        self.parent = None
        self.cost = None

    def add_action(self, action):
        if not action in self.actions:
            self.actions.append(action)

    def mark_visited(self):
        self.visited = True

    def mark_unvisited(self):
        self.visited = False

    def was_visited(self):
        return self.visited

    def was_reached(self):
        return self.cost is not None or self.parent is not None
    
    def set_parent(self, value):
        self.parent = value

    def set_cost(self, cost):
        self.cost = cost

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return f"{self.value} -> {self.actions}"

class StatesSpace:
    def __init__(self):
        self.space = {}

    def add_state(self, value):
        self.space[value] = State(value)

    def add_action(self, value1, value2):
        self.space[value1].add_action(value2)

    def get_state(self, value):
        if type(value) == tuple:
            return self.space[value[0]]
        else:
            return self.space[value]

    def reset(self):
        self.reset_visited()
        self.reset_costs()

    def reset_costs(self):
        for state in self.space.values():
            state.set_cost(None)

    def reset_visited(self):
        for state in self.space.values():
            state.mark_unvisited()

    def __str__(self):
        return "\n".join(str(state) for state in self.space.values())



class Searcher:
    def __init__(self, space, debug=False):
        self.space = space
        self.debug = debug

    def depth_first(self, intial_value, goal_value):
        return self.search(intial_value, goal_value, frontier=Stack())

    def breadth_first(self, intial_value, goal_value):
        return self.search(intial_value, goal_value, frontier=Queue())
    
    def uniform_cost(self, intial_value, goal_value):
        return self.weighted_search(intial_value, goal_value, frontier=PrioritizedQueue())

    def search(self, intial_value, goal_value, frontier):
        initial_state = self.space.get_state(intial_value)
        frontier.put(initial_state)

        while not frontier.empty():
            current_state = frontier.get()
            if self.debug: print(current_state)
            current_state.mark_visited()

            if current_state.value == goal_value:
                return self.build_solution_path(current_state)

            for action in current_state.actions:
                next_state = self.space.get_state(action)
                if not next_state.was_visited() and not frontier.has(next_state):
                    next_state.set_parent(current_state)
                    frontier.put(next_state)

    def weighted_search(self, intial_value, goal_value, frontier):
        initial_state = self.space.get_state(intial_value)
        initial_state.set_cost(0)
        frontier.put((initial_state, 0))

        while not frontier.empty():
            current_state, current_cost = frontier.get()
            current_state.mark_visited()
            if self.debug: print(current_state.value, current_cost)

            if current_state.value == goal_value:
                if self.debug: print("Goal found")
                return self.build_solution_path(current_state), current_cost

            for action in current_state.actions:
                next_state = self.space.get_state(action)
                action_cost = current_cost + action[1]

                if not next_state.was_reached() or action_cost < next_state.cost:
                    next_state.set_parent(current_state)
                    next_state.set_cost(action_cost)

                    if self.debug:print("Expanding:", next_state.value, action_cost)
                    frontier.put((next_state, action_cost))

        return []

    def build_solution_path(self, state):
        path = []
        while state:
            path.append(state.value)
            state = state.parent
        return list(reversed(path))




if __name__ == "__main__":
    debugging = False
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

    space = StatesSpace()

    state_values = space_dict.keys()
    for state_value in state_values:
        space.add_state(state_value)

    for state_value, state_actions in space_dict.items():
        for action in state_actions:
            space.add_action(state_value, action)

    searcher = Searcher(space, debug=debugging)

    initial_value = 'A'
    goal_value = 'F'
    print("Buscando camino de", initial_value, "a", goal_value, "\n")

    # print("Buscar en profundidad")
    # path = searcher.depth_first(initial_value, goal_value)
    # print(path)

    # space.reset()

    # print("Buscar en amplitud")
    # path = searcher.breadth_first(initial_value, goal_value)
    # print(path)

    space.reset()

    print("Buscar en costo uniforme")
    path, cost = searcher.uniform_cost(initial_value, goal_value)
    print(path, "costo:", cost)
