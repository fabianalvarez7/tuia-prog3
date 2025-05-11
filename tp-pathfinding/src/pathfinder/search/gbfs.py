from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


# Función heurística: distancia de Manhattan 
def heuristica(node: Node, objetivo: tuple[int, int]) -> int:
    """
    Estimación del menor costo de camino desde el estado de n a un estado objetivo.
    
    Heurística elegida:
    Distancia de Manhattan = |x_actual - x_objetivo| + |y_actual - y_objetivo|

    Argumentos:
        node (Node): el nodo actual del cual nos interesa el estado (tupla[int, int])
        objetivo: una tupla que indica la posición del estado objetivo
    Retorno:
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
        # Inicializa un nodo con la posición inicial
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None) 

        # Inicializa la frontera con el nodo inicial
        # La frontera es una cola de prioridad
        frontier = PriorityQueueFrontier()
        frontier.add(node, heuristica(node, grid.end))

        # Inicializa el diccionario de estados explorados
        explored = {} 
        # Agrega el estado del nodo inicial al diccionario de explorados
        explored[node.state] = node.cost
        
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()

            # Retorna si el nodo actual contiene el estado objetivo
            if node.state == grid.end:  # test-objetivo
                return Solution(node, explored)
            
            # Genera un diccionario con los estados de los nodos vecinos
            succesors = grid.get_neighbours(node.state)

            for action in succesors:
                new_state = succesors[action]   # función resultado
                new_cost = node.cost + grid.get_cost(new_state)

                # Chequea si el sucesor no está en explored
                if new_state not in explored or new_cost < explored[new_state]:

                    # Inicializa el nodo hijo
                    new_node = Node(value="",
                                    state=new_state,
                                    cost=new_cost,
                                    parent=node,
                                    action=action)
                    
                    # Marca el estado del nodo sucesor como explorado
                    explored[new_state] = new_cost

                    # Agrega el nuevo nodo a la frontera
                    frontier.add(new_node, heuristica(new_node, grid.end))
