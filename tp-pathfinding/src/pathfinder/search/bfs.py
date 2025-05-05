from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Inicializa un nodo con la posición inicial
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None)
        
        # Inicializa la frontera con el nodo inicial
        # La frontera es una cola
        frontier = QueueFrontier()
        frontier.add(node)

        # Inicializa el diccionario de estados explorados
        explored = {} 
        # Agrega el estado del nodo inicial a explored con el valor 'True'
        explored[node.state] = True

        while True:

            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.remove()
            
            # Retorna si el nodo actual contiene el estado objetivo
            if node.state == grid.end:
                return Solution(node, explored)
            
            # Genera un diccionario con los estados de los nodos vecinos
            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]  # función resultado
                
                # Chequea si el sucesor no está en explorados
                if new_state not in explored:

                    # Inicializa el nodo hijo
                    new_node = Node(value="",
                                    state=new_state,
                                    cost=node.cost + grid.get_cost(new_state), # función costo individual
                                    parent=node,
                                    action=action)

                    # Retorna si el nodo contiene el estado objetivo.
                    # El test-objetivo se ejecuta antes de agregar
                    # un nuevo nodo a la frontera.
                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    # Marca el estado del nodo sucesor como explorado
                    explored[new_state] = True
                    # Agrega el nuevo nodo a la frontera
                    frontier.add(new_node)