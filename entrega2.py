from itertools import combinations

from simpleai.search import CspProblem, backtrack

#4 tipos de mejoras
variables_problema = [ 
    "Mejora_Bateria",
    "Mejora_Movilidad",
    "Mejora_Suministro",
    "Mejora_Comunicacion"
]
dominios = {}
#tipo de bateria, aumento de bateria, aumento del consumo
dominios["Mejora_Bateria"] = [
    ("baterias_chicas",5000,10),
    ("baterias_medianas",7500, 20),
    ("baterias_grandes",10000,50)
    ]
#tipo de movilidad, 0 aumento de bateria, aumento de consumo
dominios["Mejora_Movilidad"] = [
    ("patas_extras",0,15),
    ("mejores_motores",0,25),
    ("orugas",0,50)
    ]           
#tipo de caja,0 aumento de bateria,aumento de consumo
dominios["Mejora_Suministro"] = [
    ("caja_superior",0,10),
    ("caja_trasera",0,10)
    ] 
#tipo de comunicacion, 0 aumento de bateria, aumento del consumo
dominios["Mejora_Comunicacion"] = [
    ("radios",0,5),
    ("video_llamadas",0,10)
    ] 

#RESTRICCIONES  
restricciones = []
# # ver que los valores sean diferentes
# def valores_diferentes(variables, values):
#     mejora1, mejora2 = values
#     return mejora1 != mejora2

# # Restricción para que las estaciones no tengan asigados los mismos barrios
# for variable1, variable2 in combinations(variables_problema, 2):
#     restricciones.append(((variable1, variable2), valores_diferentes))

# Restricción para que cuando haya baterias grandes, tambien haya orugas
def bateria_grande_requiere_oruga(variables, values):
    hay_baterias_grandes = "baterias_grandes" in [mejora[0] for mejora in values]
    hay_oruga = "oruga" in [mejora[0] for mejora in values]
    if hay_baterias_grandes:
        return hay_oruga
    else:
        return True

restricciones.append((variables_problema,bateria_grande_requiere_oruga))

# Restricción para que cuando haya suministro en la caja trasera, 
# no haya patas extras, porque se ubican en el mismo lugar.
def caja_trasera_incompatible_con_patas_extras(variables, values):
    hay_caja_trasera = "caja_trasera" in [mejora[0] for mejora in values]
    hay_patas_extras = "patas_extras" in [mejora[0] for mejora in values]
    if hay_caja_trasera:
        return not hay_patas_extras
    else:
        return True

restricciones.append((variables_problema,caja_trasera_incompatible_con_patas_extras))

# Restricción para que cuando haya radios, 
# no haya mejores motores, porque generan interferencia.
def radios_incompatible_con_mejores_motores(variables, values):
    hay_radios = "radios" in [mejora[0] for mejora in values]
    hay_mejores_motores = "mejores_motores" in [mejora[0] for mejora in values]
    if hay_radios:
        return not hay_mejores_motores
    else:
        return True

restricciones.append((variables_problema,radios_incompatible_con_mejores_motores))

# Restricción para que cuando haya videos llamadas, 
# solo se pueda elegir orugas o patas extras ya que hacen que el movimiento sea más delicado.
def video_llamadas_incompatible_con_mejores_motores(variables, values):
    hay_video_llamadas = "video_llamadas" in [mejora[0] for mejora in values]
    hay_mejores_motores = "mejores_motores" in [mejora[0] for mejora in values]
    if hay_video_llamadas:
        return not hay_mejores_motores
    else:
        return True

restricciones.append((variables_problema,video_llamadas_incompatible_con_mejores_motores))

#Restriccion para que la eleccion de las mejoras cumpla con el objetivo 
# de que las mejoras sean de al menos 50 minutos
def autonomia_es_suficiente(variables, values):
    carga = sum(mejora[1] for mejora in values)
    consumo = sum(mejora[2] for mejora in values)

    autonomia = (carga/consumo)>= 50
    return autonomia
    
restricciones.append((variables_problema,autonomia_es_suficiente))

#def rediseñar_robot():
problema = CspProblem(variables_problema, dominios, restricciones)
solucion = backtrack(problema) 
adaptaciones = solucion.items
print(adaptaciones)

