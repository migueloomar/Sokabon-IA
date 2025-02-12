import heapq

class SokobanState:
    def __init__(self, player, boxes, cost=0, parent=None, move=None):
        self.player = player  # (row, col) del jugador
        self.boxes = frozenset(boxes)  # Conjunto de posiciones de cajas
        self.cost = cost  # Costo g(n)
        self.parent = parent  # Estado padre
        self.move = move  # Movimiento realizado
        self.heuristic = self.calculate_heuristic()  # h(n)
    
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
    def calculate_heuristic(self):
        # Suma de distancias Manhattan de cada caja a su objetivo
        return sum(min(abs(bx - gx) + abs(by - gy) for gx, gy in goals) for bx, by in self.boxes)
    
    def get_successors(self):
        successors = []
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        
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
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, start_state)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.boxes == goals:
            path = []
            while current:
                path.append(current.move)
                current = current.parent
            return path[::-1][1:]
        
        closed_set.add((current.player, current.boxes))
        
        for successor in current.get_successors():
            if (successor.player, successor.boxes) in closed_set:
                continue
            heapq.heappush(open_set, successor)
    
    return None  # No hay solución

# Definir el grid y los estados iniciales
grid = [
    "######",
    "# P  #",
    "# BB #",
    "# G  #",
    "# G  #",
    "######" ]

goals = {(3, 2), (4, 2)}
initial_player = (1, 2)
initial_boxes = {(2, 2), (2, 3)}

start_state = SokobanState(initial_player, initial_boxes)
solution = a_star_sokoban(start_state)
print("Solution:", solution)
