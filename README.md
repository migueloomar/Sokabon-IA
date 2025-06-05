# Resolución de Sokoban y Puzzle de 8 Fichas con A*

Este repositorio contiene dos implementaciones del algoritmo **A\*** para resolver dos tipos distintos de puzzles:

- 🧱 **Sokoban**: un clásico juego de empujar cajas hacia objetivos.
- 🧩 **Puzzle de 8 fichas**: un tablero 3x3 con números del 1 al 8 y un espacio vacío.

---

## 🧱 Sokoban Solver

Este script resuelve automáticamente un nivel del juego **Sokoban** utilizando el algoritmo de búsqueda A*.

### Características

- Modela el estado del juego con:
  - La posición del jugador.
  - Las posiciones de las cajas.
- Genera todos los movimientos válidos, incluyendo el empuje de cajas.
- Utiliza una **heurística basada en la distancia Manhattan** desde cada caja hasta el objetivo más cercano.
- Encuentra la **secuencia mínima de movimientos** que coloca todas las cajas en sus posiciones objetivo.

---

## 🧩 8-Puzzle Solver

Este script resuelve el clásico **8-puzzle**, que consiste en ordenar los números del 1 al 8 en un tablero 3x3 moviendo una ficha vacía.

### Características

- Usa el algoritmo de búsqueda A* para explorar los posibles movimientos desde el estado inicial hasta el objetivo.
- Evalúa cada estado con una **heurística basada en la distancia Manhattan** de cada ficha a su posición correcta.
- Encuentra la **secuencia óptima de movimientos** para resolver el puzzle.

---

## ⚙️ Requisitos

- Python 3.x
- No requiere librerías externas. Solo se usa `heapq` de la biblioteca estándar.

---

## ▶️ Ejecución

Ambos scripts pueden ejecutarse directamente con Python:

```bash
python sokoban1.py
python sokoban2.py
python sokoban3.py
python 8_puzzle.py
