'''
Este código busca resolver automáticamente un nivel del juego Sokoban utilizando el algoritmo de búsqueda A*. 
Modela el estado del juego con la posición del jugador y las cajas, genera posibles movimientos válidos (incluyendo empujar cajas), 
evalúa cada estado con una heurística basada en la distancia Manhattan a los objetivos, 
y explora sistemáticamente los estados para encontrar la secuencia mínima de movimientos que lleve a todas las cajas 
a sus posiciones objetivo, devolviendo la solución si existe.
'''

# Importa la librería heapq para manejar una cola de prioridad utilizada en el algoritmo A*.
import heapq

# Define la clase SokobanState que representa un estado del juego Sokoban, almacenando la posición del jugador, 
# las posiciones de las cajas, el costo acumulado, el estado padre, el movimiento que llevó a este estado y la heurística para A*.
class SokobanState:
    def __init__(self, player, boxes, cost=0, parent=None, move=None):
        self.player = player  
        self.boxes = frozenset(boxes) 
        self.cost = cost  
        self.parent = parent  
        self.move = move  
        self.heuristic = self.calculate_heuristic()  # h(n)
        
    # Define el método __lt__ para comparar estados en la cola de prioridad según la función 
    # f(n) = g(n) + h(n), donde g(n) es el costo y h(n) la heurística.
    def __lt__(self, other):
        """ Priority queue comparison based on f(n) = g(n) + h(n) """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
        
    # Calcula la heurística como la suma de las distancias Manhattan mínimas entre cada caja y 
    # cualquiera de las posiciones objetivo, para estimar cuán cerca está el estado de la solución.
    def calculate_heuristic(self):
        return sum(min(abs(bx - gx) + abs(by - gy) for gx, gy in goals) for bx, by in self.boxes)

    # Genera todos los estados sucesores válidos a partir del estado actual, intentando mover al jugador en cada dirección y empujando cajas si es posible, 
    # ignorando movimientos inválidos (como chocar con paredes o empujar cajas contra otras cajas o paredes).
    def get_successors(self):
        successors = []
        moves = {"Arriba": (-1, 0), "Abajo": (1, 0), "Izquierda": (0, -1), "Derecha": (0, 1)}
        
        for move, (dr, dc) in moves.items():
            new_player = (self.player[0] + dr, self.player[1] + dc)
            
            if grid[new_player[0]][new_player[1]] == "#":
                continue  # No se puede mover a una pared
            
            new_boxes = set(self.boxes)
            if new_player in self.boxes:  # Si hay una caja, intentar empujarla
                new_box = (new_player[0] + dr, new_player[1] + dc)
                if new_box in self.boxes or grid[new_box[0]][new_box[1]] == "#":
                    continue  # No se puede empujar
                new_boxes.remove(new_player)
                new_boxes.add(new_box)
            
            successors.append(SokobanState(new_player, new_boxes, self.cost + 1, self, move))
        
        return successors
        
# Implementa el algoritmo A para encontrar la secuencia de movimientos que lleve desde el estado inicial a la solución, 
# utilizando una cola de prioridad para explorar estados y un conjunto para evitar estados ya visitados.*
def a_star_sokoban(start_state):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, start_state)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.boxes == goals:  # Revisar si todas las cajas están en los objetivos
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]
        
        closed_set.add((current.player, current.boxes))
        
        for successor in current.get_successors():
            if (successor.player, successor.boxes) in closed_set:
                continue
            heapq.heappush(open_set, successor)
    
    return None  # No hay solución

# Define el mapa del nivel Sokoban como una lista de cadenas, la posición objetivo, 
# la posición inicial del jugador y las posiciones iniciales de las cajas.
grid = [
    "########",
    "# P    #",
    "# BB G #",
    "### B  #",
    "#G G   #",
    "########" ]

goals = {(2, 5), (4, 1), (4, 3)}             # objetivo
initial_player = (1, 2)                      # posicion inicial player
initial_boxes = {(2, 2), (2, 3), (3, 4)}     # posicion inicial boxes

# Crea el estado inicial, ejecuta la búsqueda A, y muestra la solución encontrada como una lista de movimientos.*
start_state = SokobanState(initial_player, initial_boxes)
solution = a_star_sokoban(start_state)
print("Solution:", solution)
