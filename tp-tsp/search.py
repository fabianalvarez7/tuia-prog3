"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    
    def __init__(self, restarts=10):
        self.restarts = restarts  # Cantidad de reinicios aleatorios que vamos a hacer.

    def solve(self, problem):
        start = time()
        self.value = float('-inf')  # Inicializamos el mejor valor posible.
        self.tour = None
        self.niters = 0  # Contador global de iteraciones (suma de todas las ejecuciones).

        for a in range(self.restarts):  # Repetimos varias veces...
            random_state = problem.random_reset()
            # Elegimos un nuevo estado inicial aleatorio (otro orden de ciudades).

            problem.init = random_state
            # ⚙ Reemplazamos el estado inicial para que HillClimbing lo use.

            local = HillClimbing()
            local.solve(problem)
            # 🚀 Ejecutamos HillClimbing con ese estado aleatorio.

            self.niters += local.niters  # Acumulamos las iteraciones totales.

            if local.value > self.value:
                # Si la nueva solución es mejor que la mejor global, la guardamos.
                self.value = local.value
                self.tour = local.tour

        end = time()
        self.time = end - start  # Calculamos tiempo total.

        

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    # COMPLETAR
