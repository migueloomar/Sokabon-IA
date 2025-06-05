'''
Este código implementa un solucionador automático para el puzzle de 8 fichas (un tablero 3x3 con números del 1 al 8 y un espacio vacío). 
Usa el algoritmo de búsqueda A* para encontrar la secuencia óptima de movimientos que lleva desde un estado inicial 
desordenado hasta el estado objetivo ordenado, evaluando cada estado con una heurística basada en la distancia Manhattan para guiar la búsqueda eficientemente.
'''

# Importación del módulo heapq para manejo de colas de prioridad
import heapq

# Definición de la clase PuzzleState que representa un estado del tablero del puzzle 8
class PuzzleState:
    def __init__(self, board, parent=None, move=None, cost=0):
        self.board = board          # Board as a tuple of tuples
        self.parent = parent        # Parent state
        self.move = move            # Move taken to reach this state
        self.cost = cost            # g(n): Cost from the start node
        self.heuristic = self.calculate_manhattan()  # h(n)
        
    # Definición del método para comparación entre estados basado en f(n) = g(n) + h(n), necesario para la cola de prioridad   
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
        
    # Método para calcular la heurística h(n) usando la distancia Manhattan de cada ficha a su posición objetivo
    def calculate_manhattan(self):
        goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                          4: (1, 0), 5: (1, 1), 6: (1, 2),
                          7: (2, 0), 8: (2, 1), 0: (2, 2)}
        distance = 0
        for r in range(3):
            for c in range(3):
                tile = self.board[r][c]
                if tile != 0: 
                    goal_r, goal_c = goal_positions[tile]
                    distance += abs(goal_r - r) + abs(goal_c - c)
        return distance
        
    # Método que genera todos los estados sucesores válidos moviendo la casilla vacía
    def get_successors(self):
        successors = []
        r, c = next((r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0)
        moves = {'Up': (r - 1, c), 'Down': (r + 1, c), 'Left': (r, c - 1), 'Right': (r, c + 1)}
        
        for move, (new_r, new_c) in moves.items():
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_board = [list(row) for row in self.board] 
                new_board[r][c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[r][c]
                successors.append(PuzzleState(tuple(tuple(row) for row in new_board), self, move, self.cost + 1))
        return successors
        
# Función principal que implementa el algoritmo A para resolver el puzzle*
def a_star_puzzle(start_board, goal_board):
    """ A* Search for solving the 8-Puzzle """
    open_set = []
    closed_set = set()
    
    start_state = PuzzleState(start_board)
    heapq.heappush(open_set, start_state)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current.board == goal_board:
            path = []
            while current:
                path.append(current.move)
                current = current.parent
            return path[::-1][1:]  
        
        closed_set.add(current.board)
        
        for successor in current.get_successors():
            if successor.board in closed_set:
                continue
            heapq.heappush(open_set, successor)
    
    return None  

# Example Usage
start_state = ((8, 2, 0),
               (3, 4, 7),
               (5, 1, 6))  # Initial scrambled state

goal_state = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))  # Goal state

solution_path = a_star_puzzle(start_state, goal_state)
print("Solution Path:", solution_path)
