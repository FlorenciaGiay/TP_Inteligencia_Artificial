from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    # informed search
    greedy,
    astar,
)

from simpleai.search.viewers import WebViewer, BaseViewer

# Método para convertir tuplas a listas  
def convertir_a_listas(tuplas):
    return [list(x) for x in tuplas]

# Método para convertir listas a tuplas
def convertir_a_tuplas(listas):
    return tuple([tuple(x) for x in listas])


def planear_escaneo(tuneles, robots):

    # El estado inicial es una tupla que contiente:
    # - una tupla de tuplas de los túneles recorridos 
    # - una tupla de tuplas con el tipo de robot, la posición que también es tupla, y la batería (1000 escaneadores, 2000 soporte)

    # El segundo elemento del estado inicial es una lista ya que se debe modificar
    estado_inicial = ((),[]) 

    for robot in robots:
        if(robot[1] == "escaneador"):
            estado_inicial[1].append((robot[0], (5,0), 1000))
        else:
            estado_inicial[1].append((robot[0], (5,0), 2000))
   
    estado_inicial = convertir_a_tuplas(estado_inicial)


    # Clase problem
    class ExploracionRobotica(SearchProblem):

        # El costo es el tiempo en minutos
        def cost(self, state1, action, state2):
            robot, tipo_accion, destino_accion = action
            if(tipo_accion == 'mover'):
                return 1
            else:
                return 5
        
        def actions(self, state):
            # Las acciones son tuplas de 3 elementos: (robot, tipo_accion, destino_accion)
            # tipo_accion: mover o cargar
            # destino accion: posición a moverse (1,1) o el robot a cargar (e1)
            acciones_disponibles = []

            # Desglosar el estado en los tuneles recorridos y en los robots con su información
            tuneles_recorridos, estado_robots = state

            for robot in estado_robots:

                # Desglosar la información de los robots
                id_robot, posicion, bateria = robot
                
                if bateria >= 100:
                    posiciones_posibles = []
                    posiciones_posibles.append((posicion[0]-1, posicion[1]))
                    posiciones_posibles.append((posicion[0]+1, posicion[1]))
                    posiciones_posibles.append((posicion[0], posicion[1]-1))
                    posiciones_posibles.append((posicion[0], posicion[1]+1))

                    # Generar acciones de tipo mover con las posiciones que sean túneles
                    for posicion_posible in posiciones_posibles:
                        if posicion_posible in tuneles:
                            acciones_disponibles.append((id_robot, 'mover', posicion_posible))

                # Si el robot es de soporte (batería = 2000) generar acciones de tipo carga 
                # para los robots escaneadores que necesitan carga y están en la misma posición que el de soporte 
                if(bateria == 2000):
                    for robot_a_cargar in estado_robots:
                        # Desglosar la información de los robots a cargar
                        # id_robot_a_cargar, posicion_a_cargar, bateria_a_cargar = robot_a_cargar

                        if robot_a_cargar[1] == posicion and robot_a_cargar[2] < 1000:
                            acciones_disponibles.append((id_robot, 'cargar', robot_a_cargar[0]))

            return acciones_disponibles

        def result(self, state, action):
            # Desglosar el estado en los túneles recorridos y en los robots con su información
            tuneles_recorridos, estado_robots = state

            # Convertir a lista la tupla de túneles recorridos para luego poder modificarla (agregar)
            tuneles_recorridos = list(tuneles_recorridos)
            
            # Convertir a listas las tuplas de estado robots para luego poder modificarlas
            estado_robots = convertir_a_listas(estado_robots)
            
            # Desglosar la información de la acción
            robot, tipo_accion, destino_accion = action

            if(tipo_accion == 'mover'):
                # Modificar el estado asignándole al robot correspondiente la nueva posición
                for robot_a_mover in enumerate(estado_robots):
                    indice = robot_a_mover[0]
                    
                    if robot_a_mover[1][0] == robot:
                        estado_robots[indice][1] = destino_accion
                        
                        # Si es escaneador restar 100 a la batería
                        if robot_a_mover[1][2] != 2000:
                            estado_robots[indice][2] -= 100

                            # Agregar la coordenada del túnel que se está escaneando a 
                            # la lista de tuneles recorridos
                            if destino_accion not in tuneles_recorridos:
                                tuneles_recorridos.append(destino_accion)
            else:
                # Si el tipo de acción es cargar, modificar la batería del robot que se quiere cargar a 1000
                for robot_a_cargar in enumerate(estado_robots):
                    indice = robot_a_cargar[0]
                    if robot_a_cargar[1][0] == destino_accion:
                        estado_robots[indice][2] = 1000        
                
            tuneles_recorridos = tuple(tuneles_recorridos)
            estado_robots = convertir_a_tuplas(estado_robots)

            return (tuneles_recorridos, estado_robots)
        
        def is_goal(self, state):
            # Retornar true si el largo de túneles recorridos y túneles es igual,
            # lo que significa que se escanearon todas las posiciones del túnel
            tuneles_recorridos, estado_robots = state
            return len(tuneles_recorridos) == len(tuneles)
        
        def heuristic(self, state):
            # La heurística es la cantidad de túneles que faltan recorrer multiplicados por 1 minuto
            # tuneles_recorridos, estado_robots = state
            # return (len(tuneles) - len(tuneles_recorridos)) * 1
            
            tuneles_recorridos, estado_robots = state

            robots_bateria_cero = 0
            cantidad_robots = len(estado_robots)

            for robot in estado_robots:
                if(robot[2]<100):
                    robots_bateria_cero = robots_bateria_cero + 1

            costo = (len(tuneles) - len(tuneles_recorridos)) * 1
            # Si todos los robots quedaron en menos de 100 de bateria y todavia no se recorrieron los tuneles minimo una vez se tiene que cargar un robot
            if (robots_bateria_cero == cantidad_robots and len(tuneles) != len(tuneles_recorridos)):
                costo = costo + 5

            return costo

        
    problema = ExploracionRobotica(estado_inicial)

    resultado = astar(problema, graph_search=True)

    plan = []

    # Recorrer el resultado agregando a la lista plan, las acciones seleccionadas por el algoritmo
    for action, state in resultado.path():
        # Descartar la primera acción que es None
        if (action is not None):
            plan.append(action)

    return plan


# Prueba 

# tuneles = ( (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6) )

# robots = ( ("e1", "escaneador"), 
#             ("e2", "escaneador"), 
#             ("e3", "escaneador"), 
#             ("s1", "soporte"), 
#             ("s2", "soporte"))


tuneles = (
    (3, 3),
    (4, 3),
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (6, 3),
    (7, 3),
)

robots = ( ("e1", "escaneador"), ("s1", "soporte"),  )


resultado = planear_escaneo(tuneles, robots)

print(resultado)