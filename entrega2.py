from itertools import combinations

from simpleai.search import CspProblem, backtrack

# 4 tipos de mejoras
variables_problema = [ 
    "Mejora_Bateria",
    "Mejora_Movilidad",
    "Mejora_Suministro",
    "Mejora_Comunicacion"
]
dominios = {}

# Los valores del dominio para mejora batería están conformados por una tupla que contiene:
# tipo de batería, aumento de batería, aumento del consumo
dominios["Mejora_Bateria"] = [
    ("baterias_chicas",5000,10),
    ("baterias_medianas",7500,20),
    ("baterias_grandes",10000,50)
    ]

# Los valores del dominio para mejora movilidad están conformados por una tupla que contiene:
# tipo de movilidad, 0 aumento de batería, aumento de consumo
dominios["Mejora_Movilidad"] = [
    ("patas_extras",0,15),
    ("mejores_motores",0,25),
    ("orugas",0,50)
    ] 

# Los valores del dominio para mejora suministro están conformados por una tupla que contiene:     
# tipo de caja, 0 aumento de batería, aumento de consumo
dominios["Mejora_Suministro"] = [
    ("caja_superior",0,10),
    ("caja_trasera",0,10)
    ] 

# Los valores del dominio para mejora comunicación están conformados por una tupla que contiene:
# tipo de comunicación, 0 aumento de batería, aumento del consumo
dominios["Mejora_Comunicacion"] = [
    ("radios",0,5),
    ("videollamadas",0,10)
    ] 

# RESTRICCIONES  
restricciones = []

# Restricción para que cuando haya baterías grandes, también haya orugas
def bateria_grande_requiere_oruga(variables, values):
    hay_baterias_grandes = "baterias_grandes" in [mejora[0] for mejora in values]
    hay_oruga = "oruga" in [mejora[0] for mejora in values]
    if hay_baterias_grandes:
        return hay_oruga
    else:
        return True

restricciones.append((variables_problema,bateria_grande_requiere_oruga))

# Restricción para que cuando haya suministro en la caja trasera, 
# no haya patas extras, porque se ubican en el mismo lugar
def caja_trasera_incompatible_con_patas_extras(variables, values):
    hay_caja_trasera = "caja_trasera" in [mejora[0] for mejora in values]
    hay_patas_extras = "patas_extras" in [mejora[0] for mejora in values]
    if hay_caja_trasera:
        return not hay_patas_extras
    else:
        return True

restricciones.append((variables_problema,caja_trasera_incompatible_con_patas_extras))

# Restricción para que cuando haya radios, 
# no haya mejores motores, porque generan interferencia
def radios_incompatible_con_mejores_motores(variables, values):
    hay_radios = "radios" in [mejora[0] for mejora in values]
    hay_mejores_motores = "mejores_motores" in [mejora[0] for mejora in values]
    if hay_radios:
        return not hay_mejores_motores
    else:
        return True

restricciones.append((variables_problema,radios_incompatible_con_mejores_motores))

# Restricción para que cuando haya videollamadas, 
# solo se pueda elegir orugas o patas extras ya que hacen que el movimiento sea más delicado
def videollamadas_incompatible_con_mejores_motores(variables, values):
    hay_videollamadas = "videollamadas" in [mejora[0] for mejora in values]
    hay_mejores_motores = "mejores_motores" in [mejora[0] for mejora in values]
    if hay_videollamadas:
        return not hay_mejores_motores
    else:
        return True

restricciones.append((variables_problema,videollamadas_incompatible_con_mejores_motores))

# Restricción para que la elección de las mejoras cumpla con el objetivo 
# de que las mejoras sean de al menos 50 minutos
def autonomia_es_suficiente(variables, values):
    carga = sum(mejora[1] for mejora in values)
    consumo = sum(mejora[2] for mejora in values)

    autonomia = (carga/consumo)>= 50
    return autonomia
    
restricciones.append((variables_problema,autonomia_es_suficiente))

# Función requerida que retorna las adaptaciones seleccionadas
def rediseñar_robot():
    problema = CspProblem(variables_problema, dominios, restricciones)
    solucion = backtrack(problema) 
    solucion = list(solucion.values())
    solucion_adaptaciones = []
    for adaptacion, carga, consumo in solucion:
        solucion_adaptaciones.append(adaptacion)
    return solucion_adaptaciones
