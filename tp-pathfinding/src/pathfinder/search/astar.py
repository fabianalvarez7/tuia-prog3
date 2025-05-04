from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from ..search.gbfs import heuristica


def evaluacion(node: Node, objetivo: tuple[int, int]) -> int:
    """
    Estima el costo de una solución sumando el costo de camino de un nodo y su valor heurístico
    
    Args:
        node (Node): el nodo a evaluar.
        objetivo (tuple[int, int]): la posición del estado objetivo.
    Returns:
        El valor de evaluación del nodo. 
    """
    return node.cost + heuristica(node, objetivo)


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None)
        # Asigna el valor de evalucación a la distancia estimada
        node.estimated_distance = evaluacion(node, grid.end) 

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
                    new_node.estimated_distance = evaluacion(new_node, grid.end)
                    
                    # Mark the successor as reached
                    explored[new_state] = new_cost

                    # Add the new node to the frontier
                    frontier.add(new_node)

