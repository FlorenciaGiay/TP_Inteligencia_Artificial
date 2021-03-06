from simpleai.search import (
    SearchProblem,
    astar,
)

# Método para convertir tuplas a listas  
def convertir_a_listas(tuplas):
    return [list(x) for x in tuplas]

# Método para convertir listas a tuplas
def convertir_a_tuplas(listas):
    return tuple([tuple(x) for x in listas])

def planear_escaneo(tuneles, robots):

    # El estado inicial es una tupla que contiente:
    # - una tupla de tuplas de los túneles pendientes de recorrer 
    # - una tupla de tuplas con el tipo de robot, la posición que también es tupla, 
    # y la batería (1000 escaneadores, 2000 soporte)

    # El segundo elemento del estado inicial es una lista ya que se debe modificar
    
    estado_inicial = (tuneles,[])

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
            return 5
        
        def actions(self, state):
            # Las acciones son tuplas de 3 elementos: (robot, tipo_accion, destino_accion)
            # tipo_accion: mover o cargar
            # destino_accion: posición a moverse (1,1) o el robot a cargar (e1)
            acciones_disponibles = []

            # Desglosar el estado en los túneles pendientes y en los robots con su información
            tuneles_pendientes, estado_robots = state

            for robot in estado_robots:

                # Desglosar la información de los robots
                id_robot, posicion, bateria = robot
                
                # Generar las posiciones adyacentes a la posición actual del robot 
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
                # para los robots escaneadores que necesitan carga y están en la misma posición 
                # que el de soporte 
                if(bateria == 2000):
                    for robot_a_cargar in estado_robots:
                        if robot_a_cargar[1] == posicion and robot_a_cargar[2] < 1000:
                            acciones_disponibles.append((id_robot, 'cargar', robot_a_cargar[0]))

            return acciones_disponibles

        def result(self, state, action):
            # Desglosar el estado en los túneles pendientes y en los robots con su información
            tuneles_pendientes, estado_robots = state

            # Convertir a lista la tupla de túneles pendientes para luego poder modificarla (agregar)
            tuneles_pendientes = list(tuneles_pendientes)
            
            # Convertir a listas las tuplas de estado robots para luego poder modificarlas
            estado_robots = convertir_a_listas(estado_robots)
            
            # Desglosar la información de la acción
            id_robot, tipo_accion, destino_accion = action

            # Si el tipo de acción es mover, 
            # modificar el estado asignándole al robot correspondiente la nueva posición
            if(tipo_accion == 'mover'):
                robot_mover_en_lista = list(filter(lambda robot: robot[1][0] == id_robot, enumerate(estado_robots)))
                robot_mover = robot_mover_en_lista[0]
                idx_robot_mover = robot_mover[0]
                estado_robots[idx_robot_mover][1] = destino_accion

                # Si es escaneador (no de soporte) restar 100 a la batería
                if(robot_mover[1][2] != 2000):
                     estado_robots[idx_robot_mover][2] -= 100
                    # Eliminar la coordenada del túnel que se está escaneando de 
                    # la lista de túneles pendientes
                     if destino_accion in tuneles_pendientes:
                                tuneles_pendientes.remove(destino_accion)
            else:
                # Si el tipo de acción es cargar, modificar la batería del robot que se quiere cargar a 1000
                robot_cargar_en_lista = list(filter(lambda robot: robot[1][0] == destino_accion, enumerate(estado_robots)))
                robot_cargar = robot_cargar_en_lista[0]
                idx_robot_cargar = robot_cargar[0]
                estado_robots[idx_robot_cargar][2] = 1000

            # Convertir a tuplas los elementos del estado
            tuneles_pendientes = tuple(tuneles_pendientes)
            estado_robots = convertir_a_tuplas(estado_robots)

            return (tuneles_pendientes, estado_robots)
        
        def is_goal(self, state):
            # Retornar true si el largo de túneles pendientes es 0,
            # lo que significa que se escanearon todas las posiciones del túnel
            return len(state[0]) == 0
        
        def heuristic(self, state):
            # La heurística es la cantidad de túneles que faltan recorrer
            # multiplicados por 1 minuto
            return (len(state[0])) * 1
                    
    problema = ExploracionRobotica(estado_inicial)

    resultado = astar(problema, graph_search=True)

    plan = []

    # Recorrer el resultado agregando a la lista plan, 
    # las acciones seleccionadas por el algoritmo
    for action, state in resultado.path():
        # Descartar la primera acción que es None
        if (action is not None):
            plan.append(action)
    return plan
