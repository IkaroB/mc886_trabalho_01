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
        if open_list:
          for i in open_list:
            if adj.distance >= i.distance:
              break
          hq.heappush(open_list, adj)
        else:
          hq.heappush(open_list, adj)

  return None


# Algoritmo Iterative Deepening Search
def ids(problem):

  # depth-limited DFS
  def deph_limit(problem, node, depth, max_depth, seen):
    dest = problem["start_end_vertices"][1]
    if node in seen:
      return False
    if depth > max_depth:
      return False
    if node == dest:
      return True
    seen.add(node)
    for index, v in enumerate(node.visible):
      v = visibility.expand_vert(problem, v)
      node.visible[index] = v
      deph_limit(problem, v, depth + 1, max_depth, seen)

  # IDS
  depth = 0
  root = visibility.expand_vert(problem, problem["start_end_vertices"][0])
  found = False
  while not found:
    seen = set()
    depth += 1
    found = deph_limit(problem, root, 0, depth, seen)
  return seen


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
