# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import heapq as hq
import sys

import classes
import visibility


# Algoritmo Best-First Search
def bfs(problem):

  open_list = []
  closed_list = []
  hq.heapify(open_list)
  hq.heapify(closed_list)

  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  hq.heappush(open_list, root)

  while not len(open_list) > 0:
    hq.heapify(open_list)
    current = hq.heappop(open_list)
    hq.heappush(closed_list, current)
    if current == final_dest:
      path = []
      while current != root:
        path.append(current)
        current = current.parent
      path.append(root)
      return path[::-1]
    for adj in current.visible:
      if adj in closed_list:
        continue
      adj.distance = current.distance + visibility.line_length(
          classes.LineSeg(current, adj))
      if adj not in open_list:
        if adj.distance < open_list[0].distance:
          hq.heappush(open_list, adj)

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
