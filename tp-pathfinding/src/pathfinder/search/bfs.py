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
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None)
        
        # Initialize the explored dictionary to be empty
        alcanzados = {} 
        # Add the node to the alcanzados dictionary
        alcanzados[node.state] = True

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, alcanzados)
        
        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)

        # do
        while True:

            if frontier.is_empty():
                return NoSolution(alcanzados)
            
            node = frontier.remove()

            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]
                
                # Check if the successor is not reached
                if new_state not in alcanzados:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                    node.cost + grid.get_cost(new_state),
                                    parent=node, action=action)

                    # Mark the successor as reached
                    alcanzados[new_state] = True

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, alcanzados)

                    # Add the new node to the frontier
                    frontier.add(new_node)