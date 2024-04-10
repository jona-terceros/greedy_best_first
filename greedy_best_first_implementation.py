from frontiers import Stack, Queue, PrioritizedQueue
import math

class State:
    def __init__(self, value):
        self.value = value
        self.actions = []
        self.visited = False
        self.parent = None
        self.cost = None

    def add_action(self, action):
        if action not in self.actions:
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

    def depth_first(self, initial_value, goal_value):
        return self.search(initial_value, goal_value, frontier=Stack())

    def breadth_first(self, initial_value, goal_value):
        return self.search(initial_value, goal_value, frontier=Queue())
    
    def greedy_best_first(self, initial_value, goal_value):
        return self.search(initial_value, goal_value, frontier=PrioritizedQueue(), heuristic=self.manhattan_distance)

    def search(self, initial_value, goal_value, frontier, heuristic=None):
        initial_state = self.space.get_state(initial_value)
        # Necesitas pasar una tupla de (prioridad, estado)
        frontier.put((0, initial_state))  # Asignando una prioridad inicial de 0 para el estado inicial
        
        while not frontier.empty():
            priority, current_state = frontier.get()  # Ahora el método get() devuelve (prioridad, estado)
            if self.debug: print(current_state)
            current_state.mark_visited()

            if current_state.value == goal_value:
                return self.build_solution_path(current_state)

            for action in current_state.actions:
                next_state = self.space.get_state(action)
                if not next_state.was_visited() and not frontier.has(next_state):
                    next_state.set_parent(current_state)
                    # Aquí también necesitas pasar una tupla de (prioridad, estado)
                    priority = heuristic(next_state, self.space.get_state(goal_value)) if heuristic else 0

                    frontier.put((priority, next_state))

    def manhattan_distance(self, state, goal_state):
        x1, y1 = state.value
        x2, y2 = goal_state.value
        return abs(x1 - x2) + abs(y1 - y2)

    def build_solution_path(self, state):
        path = []
        while state:
            path.append(state.value)
            state = state.parent
        return list(reversed(path))

def load_labyrinth_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    labyrinth = []
    start = None
    goal = None

    for i, line in enumerate(lines):
        row = []
        for j, char in enumerate(line.strip()):
            if char == '#':
                row.append('#')
            elif char == 'A':
                row.append('A')
                start = (i, j)
            elif char == 'B':
                row.append('B')
                goal = (i, j)
            else:
                row.append(' ')
        labyrinth.append(row)

    return labyrinth, start, goal

if __name__ == "__main__":
    debugging = False

    # Load the labyrinth from file
    labyrinth, start, goal = load_labyrinth_from_file("C:\\Users\\jonat\\PracticaSistemasInteligentes\\search\\practica1_busqueda\\data\\laberynth0.txt")
    print("Loaded labyrinth:")
    for row in labyrinth:
        print(''.join(row))
    print()

    # Create space and add states and actions
    space = StatesSpace()
    for i in range(len(labyrinth)):
        for j in range(len(labyrinth[i])):
            if labyrinth[i][j] != '#':
                space.add_state((i, j))
                if i > 0 and labyrinth[i-1][j] != '#':
                    space.add_action((i, j), (i-1, j))
                if i < len(labyrinth)-1 and labyrinth[i+1][j] != '#':
                    space.add_action((i, j), (i+1, j))
                if j > 0 and labyrinth[i][j-1] != '#':
                    space.add_action((i, j), (i, j-1))
                if j < len(labyrinth[i])-1 and labyrinth[i][j+1] != '#':
                    space.add_action((i, j), (i, j+1))

    # Perform search
    searcher = Searcher(space, debug=debugging)
    print("Searching for path from", start, "to", goal)
    print("Using greedy best-first search")
    path = searcher.greedy_best_first(start, goal)
    print("Path:", path)
