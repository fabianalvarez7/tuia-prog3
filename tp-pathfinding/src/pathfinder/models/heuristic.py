from ..models.node import Node

# Función heurística: distancia de Manhattan 
def heuristic(node: Node, objetivo: tuple[int, int]) -> int:
    """
    Distancia de Manhattan = |x_actual - x_objetivo| + |y_actual - y_objetivo|

    Args:
        node (Node): el nodo actual del cual nos interesa el estado (tupla[int, int])
        objetivo: una tupla que indica la posición del estado objetivo
    Returns:
        int: la distancia de Manhattan desde el estado actual hasta el estado objetivo.
    """

    return abs(node.state[0] - objetivo[0]) + abs(node.state[1] - objetivo[1])