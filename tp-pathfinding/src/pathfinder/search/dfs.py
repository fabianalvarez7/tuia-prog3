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
        # Initialize a node with the initial position
        node = Node("", state=grid.start, coast=0, parent=None, action=None)
        
        # Initialize the explored dictionary to be empty
        expandidos = {} 

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, expandidos)    

        # Initialize the frontier with the initial node
        # In this example, the frontier is a stack
        frontier = StackFrontier()
        frontier.add(node)

        # do
        while True:

            if frontier.is_empty():
                return NoSolution(expandidos)
            
            node = frontier.remove()

            if not node.state in expandidos:  
                frontier.add(node)

            
            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]
                
                # Check if the successor is not reached
                if new_state not in expandidos:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                    node.cost + grid.get_cost(new_state),
                                    parent=node, action=action)

                    # Mark the successor as reached
                    expandidos[new_state] = True

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, expandidos)

                    # Add the new node to the frontier
                    frontier.add(new_node)