from simpleai.search import (
    SearchProblem,
    greedy,
    astar,
)

# Metodo para convertir tupla a lista
def convertir_a_lista(tupla):
    lista = list(tupla)
    return lista

# Metodo para convertir lista a tupla
def convertir_a_tupla(lista):
    tupla = tuple(lista)
    return tupla
    

def planear_escaneo(tuneles, robots):

    # El estado es una tupla de tuplas con el tipo de robot, la posicion que tambien es tupla 
    # y si es mapeador la bateria actual
    estado_inicial = []
    for robot in robots:
        if(robot[1] == 'escaneador'):
            tupla = (robot[0], (5,0), 1000)
        else:
            tupla = (robot[0], (5,0))
        estado_inicial.append(tupla)
    estado_tupla = convertir_a_tupla(estado_inicial)

    # Clase problem
    class ExploracionRobotica(SearchProblem):    

        # Lista de los tuneles que van recorriendo los robots
        tuneles_recorridos = []

        def cost(self, state1, action, state2):
            robot, tipo_accion, destino_accion = action
            if(tipo_accion == 'mover'):
                return 1
            else:
                return 5
        
        def actions(self, state):
            # Las acciones seran tuplas de 3 elementos: (robot, tipo accion, destino accion)
            # tipo accion: mover o cargar
            # destino accion: posicion a moverse (1,1) o el robot a cargar
            acciones_disponibles = []

            for elemento in state:
                accion = []

                # Si el largo de elemento es 3 siginfica que es escaneador (el tercer dato es la bateria)
                if len(elemento) == 3:
                    robot, posicion, bateria = elemento
                    if bateria >= 100:
                        posiciones_posibles = []
                        posiciones_posibles.append(posicion[0]-1, posicion[1])
                        posiciones_posibles.append(posicion[0]+1, posicion[1])
                        posiciones_posibles.append(posicion[0], posicion[1]-1)
                        posiciones_posibles.append(posicion[0], posicion[1]+1)

                        # Generar acciones de tipo mover a las posiciones que sean tuneles
                        for posicion_posible in posiciones_posibles:
                            if posicion_posible in tuneles:
                                acciones_disponibles.append((robot, 'mover', posicion_posible))

                # Si el largo de elemento no es 3 siginfica que es soporte (no tiene el dato de la bateria ya que es infinita)
                else:
                    robot, posicion = elemento 
                    posiciones_posibles = []
                    posiciones_posibles.append(posicion[0]-1, posicion[1])
                    posiciones_posibles.append(posicion[0]+1, posicion[1])
                    posiciones_posibles.append(posicion[0], posicion[1]-1)
                    posiciones_posibles.append(posicion[0], posicion[1]+1)

                    # Generar acciones de tipo mover a las posiciones que sean tuneles
                    for posicion_posible in posiciones_posibles:
                        if posicion_posible in tuneles:
                            acciones_disponibles.append((robot, 'mover', posicion_posible))
                    
                    # Generar acciones de tipo carga con los robots escaneadores que necesitan carga y 
                    # estan en la misma posicion que el robot de soporte 
                    for objeto in state:
                        if len(objeto) == 3 and objeto[1] == posicion and objeto[2] < 1000:
                            acciones_disponibles.append((robot, 'cargar', objeto[0]))

            return acciones_disponibles
                        
        def result(self, state, action):
            return state
        
        def is_goal(self, state):
            # comparar tuneles_recorridos con tuneles elemento por elemento
            # o el largo de las listas
            return 
        
        def heuristic(self, state):
            return 0
        
    problem = ExploracionRobotica(estado_inicial)

    result = astar(problem, graph_search=True)

    print("Goal node:", result)

    print("Path from initial to goal:")
    for action, state in result.path():
        print("Action:", action)
        print("State:", state)
    
    return result