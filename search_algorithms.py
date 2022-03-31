# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import heapq as hq
import sys

from numpy import append

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

  root = visibility.expand_vert(problem, root)
  hq.heappush(open_list, root)
  #hq.heapify(root.visible)

  while len(open_list) > 0:
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
    for index, adj in enumerate(current.visible):
      adj.parent = current
      adj = visibility.expand_vert(problem, adj)
      current.visible[index] = adj
      hq.heapify(current.visible)
      if adj in closed_list:
        continue
      adj.distance = current.distance + visibility.line_length(
          classes.LineSeg(current, adj))
      if adj not in open_list:
        hq.heappush(open_list, adj)

  return None


# Algoritmo Iterative Deepening Search
def ids(problem):

  # depth-limited DFS
  def deph_limit(p, node, depth):
    dest = p["start_end_vertices"][1]
    if (node == dest) and (depth == 0):
      return node
    elif node == p["start_end_vertices"][0]:
      return node
    elif depth > 0:
      child = visibility.expand_vert(p, node)
      print(child)
      for v in child.visible:
        v.parent = child
        res = deph_limit(p, v, depth - 1)
        if res != None:
          return res
    else:
      return None

  # IDS
  depth = 300
  root = problem["start_end_vertices"][0]
  dest = problem["start_end_vertices"][1]
  while True:
    path = []
    found = deph_limit(problem, problem["start_end_vertices"][0], depth)
    if found not in path:
      path.append(found)
      return path
    depth += 1


# Algoritmo A* Search
def a_star(problem):

  path = []

  return path


# Algoritmo Iterative Deepening A*
def ida_star(problem):

  path = []

  return path


def main():
  return


if __name__ == "__main__":
  main()
