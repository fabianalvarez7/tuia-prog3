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
from collections import deque


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
        super().__init__()  # LLamada al consructor de LocalSearch
        self.restarts = restarts  # Cantidad de reinicios aleatorios

    def solve(self, problem: OptProblem):
        start = time()
        self.value = float('-inf')  # Inicializamos con el peor valor posible
        self.tour = None    # Todavía no hay ningún tour
        self.niters = 0  # Contador de iteraciones

        for _ in range(self.restarts):
            # Genermos un nuevo estado aleatorio inicial
            random_state = problem.random_reset()

            # Reemplazamos el estado inicial para que HillClimbing lo use.
            problem.init = random_state
            
            # Ejecutamos HillClimbing con ese estado aleatorio.
            local = HillClimbing()
            local.solve(problem)
            
            # Acumulamos las iteraciones totales.
            self.niters += local.niters  

            # Guardamos la mejor solución
            if local.value > self.value:
                self.value = local.value
                self.tour = local.tour

        # Calculamos tiempo total de ejecución
        self.time = time() - start  

        

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def __init__(self, tabu_size=40, max_iters=1000):
        super().__init__()
        self.tabu_size = tabu_size      # Capacidad máxima de la lista tabú
        self.max_iters = max_iters      # Criterio de parada

    def solve(self, problem: OptProblem):
        start = time()
        self.niters = 0

        actual = problem.init
        mejor = actual
        valor_actual = problem.obj_val(actual)
        mejor_valor = valor_actual

        tabu = deque(maxlen=self.tabu_size)  # Cola de capacidad fija

        while self.niters < self.max_iters:
            # Mejor acción que no esté en la lista tabú
            act, succ_val = problem.max_action(actual, tabu)

            # Aplicar esa acción para generar un nuevo estado
            sucesor = problem.result(actual, act)

            # Ver si ese nuevo estado es el mejor hasta ahora
            if problem.obj_val(sucesor) > mejor_valor:
                mejor = sucesor
                mejor_valor = problem.obj_val(sucesor)

            # Agregar acción a la lista tabú
            # Esto evita que se revierta en las próximas iteraciones
            tabu.append(act)

            # Avanzar al nuevo estado, aunque sea peor
            actual = sucesor
            self.niters += 1

        # Guardamos el mejor recorrido encontrado
        self.tour = mejor
        self.value = mejor_valor
        self.time = time() - start
