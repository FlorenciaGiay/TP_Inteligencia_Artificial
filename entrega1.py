from simpleai.search import (
    SearchProblem,
    greedy,
    astar,
)

def planear_escaneo(tuneles, robots):

    class ExploracionRobotica(SearchProblem):
        
        def initial(self):
            
            return 0
        
        def cost(self, state1, action, state2):
            return 0

        def actions(self, state):
            acciones = []
            return acciones
                     
        def result(self, state, action):
            return state
        
        def is_goal(self, state):
            return 
        
        def heuristic(self, state):
            return 0
    
    result = astar(ExploracionRobotica, graph_search=True)

    return result


