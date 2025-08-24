import heapq
from typing import List, Dict

class Node:
    def _init_(self, name: str, coordinates: Dict[str, float]):
        self.name = name
        self.coordinates = coordinates

class Arc:
    def _init_(self, from_node: Node, to_node: Node, cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

class Path:
    def _init_(self, nodes: List[Node], total_cost: float):
        self.nodes = nodes
        self.total_cost = total_cost

def heuristic(node: Node, goal: Node) -> float:
    x1, y1 = node.coordinates['x'], node.coordinates['y']
    x2, y2 = goal.coordinates['x'], goal.coordinates['y']
    return ((x1 - x2) * 2 + (y1 - y2) * 2) ** 0.5

def a_star_search(start: Node, goal: Node) -> Path:
    frontier = [(0, start, [])]  # (priority, node, path)
    explored = set()

    while frontier:
        current_cost, current_node, current_path = heapq.heappop(frontier)

        if current_node == goal:
            return Path(current_path + [current_node], current_cost)

        if current_node in explored:
            continue

        explored.add(current_node)

        for arc in get_neighbors(current_node):
            neighbor = arc.to_node
            new_cost = current_cost + arc.cost
            priority = new_cost + heuristic(neighbor, goal)

            heapq.heappush(frontier, (priority, neighbor, current_path + [current_node]))

    return Path([], float('inf'))  # Nessun percorso trovato

def get_neighbors(node: Node) -> List[Arc]:
    # Implementa la logica per ottenere i vicini di un nodo
    # Ad esempio, utilizzare un modulo di prolog, chiamate API, ecc.

    neighbors = []


    def find_node(node, target_value):

        if node.value == target_value:

            if node.children and node.children[0].value != target_value:

                neighbors.extend(child.value for child in node.children)

            if node.children and node.children[-1].value != target_value:

                neighbors.extend(child.value for child in node.children)

            return True        
        
        for child in node.children:

            if find_node(child, target_value):

                return True

        return False


    find_node(tree, target_value)

    return neighbors
