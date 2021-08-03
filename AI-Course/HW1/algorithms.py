from maps import Map
from queue import PriorityQueue, Queue
import time


class Search:

    def __init__(self):
        self.count = 4

    def dfs(self, m: Map) -> list:
        start_time = time.time()

        fringe = PriorityQueue()
        fringe.put((0, m.me, [], []))

        while not fringe.empty():
            # get the most prioritised node from fringe
            depth, current, path, visited = fringe.get()

            # If current node is goal, return the path
            if m.is_goal(current[0], current[1]):
                return path + [current]

            # Visit the current node
            visited += [current]

            # Expand current node
            child_nodes = m.get_successors(current[0], current[1])
            for node in child_nodes:
                if node not in visited:
                    # If 
                    if m.is_goal(node[0], node[1]):
                        return path + [node]

                    # depth_of_node is prioritisation measure for priority queue,
                    # It must be negative to ensure that nodes with greater depth get explored before shallower ones
                    depth_of_node = len(path)
                    fringe.put((-depth_of_node, node, path + [node], visited))

        print('DFS Search')
        print('Duration:', time.time() - start_time)
        return path


    def bfs(self, m: Map) -> list:
        start_time = time.time()

        visited = []
        path = [] 
	
        queue = Queue()
        queue.put((m.me, None))

        while not queue.empty():
            # Pop from queue
            top = queue.get()
            current, parent = top
            
            # If current node is visited, ignore it
            if current in visited:
                continue

            # Visit the current node
            visited += [current]

            # If current node is goal, get the path
            if m.is_goal(current[0], current[1]): 
                goal = top
                break

            # Expand current node
            child_nodes = m.get_successors(current[0], current[1])
            for node in child_nodes:
                if node not in visited:
                    queue.put((node, top))

        # Get the path
        node = goal
        while node != None:
            path += [node[0]]
            node = node[1]

        print('BFS Search')
        print('Duration:', time.time() - start_time)
        return path[::-1]


    def uniform_cost(self, m: Map) -> list:
        start_time = time.time()

        visited = []
        path = []
        queue = PriorityQueue()
        node = (m.me, None, 1)  # start state, parent, cost
        queue.put(node, 0)   

        while not queue.empty():
            # get the most prioritised node from queue
            top = queue.get()
            current, parent, current_cost = top

            # If current node is visited, ignore it
            if current in visited:
                continue

            # Visit the current node
            visited += [current]

            if m.is_goal(current[0], current[1]):
                goal = top
                break

            # Expand current node
            child_nodes = m.get_successors(current[0], current[1])
            for node in child_nodes:
                if node not in visited:
                    # Cost is prioritisation measure for priority queue and child's cost
                    cost = 1 + current_cost
                    queue.put((node, top, cost), cost)
        
        # Get the path
        node = goal
        while node != None:
            path += [node[0]]
            node = node[1]

        print('Uninformed Search')
        print('Duration:', time.time() - start_time)
        return path[::-1]

    def get_euclidean_heuristics(self, m: Map) -> list:
        # Your Code here
        # Hint: https://en.wikipedia.org/wiki/Euclidean_distance#Two_dimensions
        # Hint: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        pass

    def get_euclidean_heuristics(self, x: int, y: int, m: Map) -> list:
        heuristics = []
        goal_lst = m.goals

        # Get euclidean heuristics from one node to all of goals
        for goal_lst_item in goal_lst:
            dx = abs(x - goal_lst_item[0])
            dy = abs(y - goal_lst_item[1])
            heuristics.append(dx - dy)

        return heuristics

    
    def a_star(self, m: Map, heuristics: list) -> list:
        start_time = time.time()

        visited = []
        path = []
        queue = PriorityQueue()
        node = (m.me, None, 1)
        queue.put(node, 0)

        # For finding goals
        _goals = set(m.goals)
        _visited_goals = set()
        _path = set()

        while not queue.empty():
            # Pop from queue
            top = queue.get()
            current, parent, current_cost = top

            # If current node is visited, ignore it
            if current in visited:
                continue

            # Visit the current node
            visited += [current]

            if current in _goals:
                _visited_goals.add(current)
                _path.add(top)

                if _visited_goals == _goals:
                    break

            # Expand current node
            child_nodes = m.get_successors(current[0], current[1])
            for node in child_nodes:
                if node not in visited:
                    # f(n) = g(n) + h(n) is prioritisation measure for priority queue and child's cost
                    # g(n) == cost
                    cost = 1 + current_cost       
                    queue.put((node, top, cost), cost + min(self.get_euclidean_heuristics(node[0], node[1], m)))

        # Get the path
        for node in _path:
            while node != None:
                path += [node[0]]
                node = node[1]

        print('A* Search')
        print('Duration:', time.time() - start_time)
        return path[::-1]
