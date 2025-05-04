from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


# Función heurística: distancia de Manhattan 
def heuristica(node: Node, objetivo: tuple[int, int]) -> int:
    """
    Distancia de Manhattan = |x_actual - x_objetivo| + |y_actual - y_objetivo|

    Args:
        node (Node): el nodo actual del cual nos interesa el estado (tupla[int, int])
        objetivo: una tupla que indica la posición del estado objetivo
    Returns:
        La distancia de Manhattan desde el estado actual hasta el estado objetivo.
    """

    return abs(node.state[0] - objetivo[0]) + abs(node.state[1] - objetivo[1])


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None)
        # Asigna la heuristica a la distancia estimada
        node.estimated_distance = heuristica(node, grid.end) 

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = node.cost
        
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)
            
            succesors = grid.get_neighbours(node.state)

            for action in succesors:
                new_state = succesors[action]
                new_cost = node.cost + grid.get_cost(new_state)

                # Check if the successor is not reached
                if new_state not in explored or new_cost < explored[new_state]:

                    # Initialize the son node
                    new_node = Node(value="",
                                    state=new_state,
                                    cost=new_cost,
                                    parent=node,
                                    action=action)
                    new_node.estimated_distance = heuristica(new_node, grid.end)
                    
                    # Mark the successor as reached
                    explored[new_state] = new_cost

                    # Add the new node to the frontier
                    frontier.add(new_node)
