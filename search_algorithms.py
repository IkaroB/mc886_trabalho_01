# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import queue
import sys


# Algoritmo Best-First Search
def bfs(problem):
  visited = queue.Queue()
  path = []

  # Marca o vértice inicial como visitado e insere na fila
  path.append(problem["start_end_vertices"][0])
  problem["start_end_vertices"][0].set_visited(True)
  visited.put(problem["start_end_vertices"][0])

  # O caminho é construído a partir da fila de vértices visitados
  while not visited.empty():
    v = visited.get()
    # Se o vértice atual é o vértice final, o caminho foi encontrado
    if v == problem["start_end_vertices"][1]:
      path.append(v)
      return path
    for adj in v.visible:
      if not adj.get_visited():
        adj.set_visited(True)
        visited.put(adj)
        path.append(adj)
  return None


# Algoritmo Iterative Deepening Search
def ids(problem):

  # depth-limited DFS
  def deph_limit(node, depth):
    if depth == 0:
      if node == problem["start_end_vertices"][1]:
        return (node, True)
      else:
        return (None, True)
    elif depth > 0:
      any_remaning = False
      for adj in node.visible:
        path, remaning = deph_limit(adj, depth - 1)
        if not path:
          return (path, True)
        if remaning:
          any_remaning = True
      return (None, any_remaning)

  # IDS
  depth = 0
  path = []
  for depth in range(sys.maxsize):
    path, remaning = deph_limit(problem["start_end_vertices"][0], depth)
    if not path:
      return path
    elif (not remaning):
      return None


# Algoritmo A* Search
def a_star(problem):

  path = []

  return path


# Algoritmo Iterative Deepening A*
def ida_star(problem):

  path = []

  return path
