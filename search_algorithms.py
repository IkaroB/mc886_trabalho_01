# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import copy
import heapq as hq

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

    for v in open_list:
      print(v.distance, v, end=' ')
    print('\nNEXT')

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
        #  if open_list:
        #for i in open_list:
        #  if adj.distance >= i.distance:
        #    break
        #    hq.heappush(open_list, adj)
        #  else:
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

  open_list = []
  closed_list = []

  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  root = visibility.expand_vert(problem, root)
  open_list.append(root)
  i = 0

  while len(open_list) > 0:
    current = open_list.pop(0)
    #print(f'CURRENT: {current.name} - DIST: {current.distance}')
    closed_list.append(current)

    if current == final_dest:
      path = []
      while current != root:
        path.append(current)
        current = current.parent
      path.append(root)

      print('BEST', end=': ')
      for p in path:
        print(f'{p.name}', end='-')
      #print('ALL VISITED', end = ': ')
      #for c in closed_list:
      #  print(f'{c.name}', end = '-')
      return

    a = copy.copy(current)
    print('PATH', end=': ')
    while a != None:
      print(f'{a.name}', end='-')
      a = a.parent
    print()

    for v in current.visible:
      children = copy.copy(v)

      children.parent = current
      children = visibility.expand_vert(problem, children)

      if children in closed_list:
        continue

      children.distance = current.distance + \
                          visibility.line_length(classes.LineSeg(current, children)) + \
                          visibility.line_length(classes.LineSeg(children, final_dest))

      #print(children.distance, children)

      if children not in closed_list:
        open_list.append(children)

    open_list.sort(key=lambda v: v.distance)

    # for v in open_list:
    #   print(v.name, end = ' ')
    # print('\n')

  return path


# Algoritmo Iterative Deepening A*
def ida_star(problem):

  path = []

  return path


def main():
  return


if __name__ == "__main__":
  main()
