from simpleai.search import (
    SearchProblem,
    greedy,
    astar,
)

# Método para convertir tuplas a listas  
def convertir_a_listas(tuplas):
    return [list(x) for x in tuplas]

# Método para convertir listas a tuplas
def convertir_a_tuplas(listas):
    return tuple([tuple(x) for x in listas])


def planear_escaneo(tuneles, robots):

    # El estado es una tupla de tuplas con el tipo de robot, la posición que también es tupla 
    # y si es mapeador la batería actual
    estado_inicial = []
    for robot in robots:
        if(robot[1] == 'escaneador'):
            tupla = (robot[0], (5,0), 1000)
        else:
            tupla = (robot[0], (5,0))
        estado_inicial.append(tupla)
        
    estado_tupla = tuple(estado_inicial)


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

            for elemento in state:
                
                # Si el largo de elemento es 3 siginfica que es escaneador (el tercer dato es la batería)
                if len(elemento) == 3:
                    robot, posicion, bateria = elemento
                    if bateria >= 100:
                        posiciones_posibles = []
                        posiciones_posibles.append((posicion[0]-1, posicion[1]))
                        posiciones_posibles.append((posicion[0]+1, posicion[1]))
                        posiciones_posibles.append((posicion[0], posicion[1]-1))
                        posiciones_posibles.append((posicion[0], posicion[1]+1))

                        # Generar acciones de tipo mover a las posiciones que sean túneles
                        for posicion_posible in posiciones_posibles:
                            if posicion_posible in tuneles:
                                accion_prueba = (robot, 'mover', posicion_posible)
                                acciones_disponibles.append(accion_prueba)

                # Si el largo de elemento no es 3 siginfica que es soporte (no tiene el dato de 
                # la batería ya que es infinita)
                else:
                    robot, posicion = elemento 
                    posiciones_posibles = []
                    posiciones_posibles.append((posicion[0]-1, posicion[1]))
                    posiciones_posibles.append((posicion[0]+1, posicion[1]))
                    posiciones_posibles.append((posicion[0], posicion[1]-1))
                    posiciones_posibles.append((posicion[0], posicion[1]+1))

                    # Generar acciones de tipo mover a las posiciones que sean túneles
                    for posicion_posible in posiciones_posibles:
                        if posicion_posible in tuneles:
                            acciones_disponibles.append((robot, 'mover', posicion_posible))
                    
                    # Generar acciones de tipo carga con los robots escaneadores que necesitan carga y 
                    # están en la misma posición que el robot de soporte 
                    for objeto in state:
                        if len(objeto) == 3 and objeto[1] == posicion and objeto[2] < 1000:
                            acciones_disponibles.append((robot, 'cargar', objeto[0]))

            return acciones_disponibles

        # Lista de los túneles que van recorriendo los robots
        tuneles_recorridos = []

        def result(self, state, action):
            estado_lista = convertir_a_listas(state)
            robot, tipo_accion, destino_accion = action

            if(tipo_accion == 'mover'):
                # Modificar el estado asignándole al robot correspondiente la nueva posición
                # y si es escaneador, le resto 100 a la batería
                for elemento in estado_lista:
                    if elemento[0] == robot:
                        elemento[1] = destino_accion
                        if len(elemento) == 3:
                            elemento[2] = elemento[2] - 100
                            
                            # Agregar la coordenada del tunel que se está escaneando a 
                            # la lista de tuneles recorridos
                            if destino_accion not in self.tuneles_recorridos:
                                self.tuneles_recorridos.append(destino_accion)
            else:
                    # Si el tipo de acción es cargar, modifico en el estado la batería del robot
                    # al que se quiere cargar a 1000
                    for elemento in estado_lista:
                        if elemento[0] == destino_accion:
                            elemento[2] = 1000        
            
            estado_tupla = convertir_a_tuplas(estado_lista)

            return  estado_tupla
        
        def is_goal(self, state):
            # Retornar true si el largo de túneles recorridos y túneles es igual,
            # lo que significa que se escanearon todas las posiciones del túnel
            condicion = len(self.tuneles_recorridos) == len(tuneles)
            return condicion
        
        def heuristic(self, state):
            # La heurística es la cantidad de túneles que faltan recorrer multiplicados por 1 minuto
            tiempo = [len(tuneles) - len(self.tuneles_recorridos)] * 1
            return tiempo

        
    problema = ExploracionRobotica(estado_tupla)

    result = astar(problema, graph_search=True)

    plan = []

    for action in result.path():
        accion = action
        plan.append(action)

    return plan


# Prueba 

# tuneles = ( (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6) )

# robots = ( ("e1", "escaneador"), 
#             ("e2", "escaneador"), 
#             ("e3", "escaneador"), 
#             ("s1", "soporte"), 
#             ("s2", "soporte"))


tuneles = ( (5, 1), )

robots = ( ("e1", "escaneador"),  )

resultado = planear_escaneo(tuneles, robots)