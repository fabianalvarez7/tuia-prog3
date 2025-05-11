from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from ..search.gbfs import heuristica


def evaluacion(node: Node, objetivo: tuple[int, int]) -> int:
    """
    Estima el costo de una solución sumando el costo de camino de un nodo y su valor heurístico.
    
    Argumentos:
        node (Node): el nodo a evaluar.
        objetivo (tuple[int, int]): la posición del estado objetivo.
    Retorno:
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
        # Inicializa un nodo con la posición inicial
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None) 

        # Inicializa la frontera con el nodo inicial
        # La frontera es una cola de prioridad
        frontier = PriorityQueueFrontier()
        frontier.add(node, evaluacion(node, grid.end))

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
                new_state = succesors[action]
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
                    frontier.add(new_node, evaluacion(node, grid.end))

