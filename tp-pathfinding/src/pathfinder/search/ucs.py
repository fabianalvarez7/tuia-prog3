from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

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
        frontier.add(node, node.cost)

        # Inicializa el diccionario de estados explorados y su costo
        explored = {}
        # Marca el estado del nodo como explorado
        explored[node.state] = node.cost
        
        while True:

            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()

            # Retorna si el nodo actual contiene el estado objetivo
            if node.state == grid.end:  # test-objetivo
                return Solution(node, explored)

            # Genera un diccionario con los estados de los nodos vecinos
            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]  # función resultado
                new_cost = node.cost + grid.get_cost(new_state)
                
                # Si el sucesor no está en explorared o si el costo es menor
                if new_state not in explored or new_cost < explored[new_state]:

                    # Inicializa el nodo hijo
                    new_node = Node(value="",
                                    state=new_state,
                                    cost=new_cost,
                                    parent=node,
                                    action=action)

                    # Marca el estado del nodo como explorado
                    explored[new_state] = new_cost
                    # Agrega el nuevo nodo a la frontera
                    frontier.add(new_node, new_cost)