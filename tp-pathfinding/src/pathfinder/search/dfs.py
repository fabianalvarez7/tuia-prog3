from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Inicializa un nodo con la posición inicial
        node = Node(value="", state=grid.start, cost=0, parent=None, action=None)

        # Retorna si el nodo contiene el estado objetivo
        if node.state == grid.end:   # test-objetivo
            return Solution(new_node, explored)
        
        # Inicializa la frontera con el nodo inicial
        # La frontera es una pila
        frontier = StackFrontier()
        frontier.add(node)

        # Inicializa el diccionario de estados explorados
        explored = {}

        while True:

            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.remove()

            # Si el estado ya fue explorado, se ignora
            if node.state in explored:
                continue

            # Marca el estado del nodo actual como explorado
            explored[node.state] = True

            # Obtiene los nodos vecinos del nodo actual
            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]  # función resultado
                
                # Chequea si el sucesor no está en explorados
                if new_state not in explored:

                    # Inicializa el nodo hijo
                    new_node = Node(value="",
                                    state=new_state,
                                    cost=node.cost + grid.get_cost(new_state),
                                    parent=node,
                                    action=action)

                    # Retorna si el nodo contiene el estado objetivo
                    if new_state == grid.end:   # test-objetivo
                        return Solution(new_node, explored)

                    # Agrega el nuevo nodo a la frontera
                    frontier.add(new_node)