import heapq

class SokobanState:
    def __init__(self, player, boxes, cost=0, parent=None, move=None):
        
        """
        Inicializa un estado del juego de Sokoban.
        
        player: Tupla (fila, columna) que representa la posición del jugador.
        boxes: Conjunto inmutable de posiciones de las cajas.
        cost: Costo acumulado del estado.
        parent: Estado padre desde el cual se llegó a este estado.
        move: Movimiento realizado para llegar a este estado.
        """
        self.player = player  
        self.boxes = frozenset(boxes) 
        self.cost = cost  
        self.parent = parent  
        self.move = move  
        self.heuristic = self.calculate_heuristic()  # h(n)
    
    def __lt__(self, other):
        """ Priority queue comparison based on f(n) = g(n) + h(n) """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
    def calculate_heuristic(self):
        # Suma de distancias Manhattan de cada caja a su objetivo
        return sum(min(abs(bx - gx) + abs(by - gy) for gx, gy in goals) for bx, by in self.boxes)
    
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

def a_star_sokoban(start_state):
    """
    Implementa el algoritmo A* para resolver el problema de Sokoban.
    
    start_state: Estado inicial del juego.
    return: Lista de movimientos que llevan a la solución o None si no hay solución.
    """
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

# Grid y los estados iniciales
grid = [
    "#####", 
    "#P  #", 
    "# B #", 
    "# G #", 
    "#####" ]

goals = {(3, 2)} # objetivo
initial_player = (1, 1) # posicion inicial player
initial_boxes = {(2, 2)} # posicion inicial boxes

start_state = SokobanState(initial_player, initial_boxes)
solution = a_star_sokoban(start_state)
print("Solution:", solution)
