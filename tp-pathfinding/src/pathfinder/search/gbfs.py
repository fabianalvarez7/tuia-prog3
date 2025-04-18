from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


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
        node = Node("", state=grid.start, coast=0, parent=None, action=None, heuristic=0)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier
        frontier.add(node, node.heuristic)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = node.heuristic
        
        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()
            if node.state == grid.end():
                return Solution(node, explored)
            
            succesors = grid.get_neighbours(node.state)

            for action in succesors:
                new_state = succesors[action]
                new_coast = node.coast + grid.get_cost(new_state)

                # Check if the successor is not reached
                if new_state not in explored or new_coast < explored[new_state]:

                    # Initialize the son node
                    new_node = Node("", state=new_state,
                                    coast=new_coast,
                                    parent=node,
                                    action=action)
                    
                    # Mark the successor as reached
                    explored[new_state] = new_coast

                    # Add the new node to the frontier
                    frontier.add(new_node, new_node.heuristic)
