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
        # Initialize a node with the initial position
        node = Node("", grid.start, cost=0, parent=None, action=None)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a priority queue
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)

        # Initialize the explored dictionary to be empty
        alcanzados = {}
        # Add the node to the alcanzados dictionary
        alcanzados[node.state] = node.cost

        # do
        while True:

            if frontier.is_empty():
                return NoSolution(alcanzados)
            
            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, alcanzados)

            successors = grid.get_neighbours(node.state)

            for action in successors:
                new_state = successors[action]
                new_cost = node.cost + grid.get_cost(new_state)
                
                # Check if the successor is not reached
                if new_state not in alcanzados or new_cost < alcanzados[new_state]:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                    new_cost,
                                    parent=node, action=action)

                    # Mark the successor as reached
                    alcanzados[new_state] = new_cost

                    # Add the new node to the frontier
                    frontier.add(new_node, new_cost)