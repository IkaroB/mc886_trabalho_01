# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import copy
from unittest import result

import classes
import visibility


# Algoritmo Best-First Search
def bfs(problem):

  i = 0
  path = []

  open_list = []
  closed_list = []

  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  root = visibility.expand_vert(problem, root)
  open_list.append(root)

  while len(open_list) > 0:
    current = open_list.pop(0)
    closed_list.append(current)

    if current == final_dest:
      path = []
      while current != root:
        path.append(current)
        current = current.parent
      path.append(root)
      return path

    a = copy.copy(current)
    while a != None:
      problem["paths"][i].append(a)
      a = a.parent
    i += 1

    for v in current.visible:
      children = copy.copy(v)

      children.parent = current
      children = visibility.expand_vert(problem, children)

      if children in closed_list:
        continue

      children.distance = current.distance + \
                          visibility.line_length(classes.LineSeg(current, children))
      if children not in closed_list:
        open_list.append(children)

    open_list.sort(key=lambda v: v.distance)
  return path


# Algoritmo Iterative Deepening Search
def ids(problem):

  def ids_search(node, target, current_depth, max_depth, path):
    if node == target:
      return node, True

    if current_depth == max_depth:
      if len(node.visible) > 0:
        return None, False
      else:
        return None, True

    bottom_reached = True
    for v in node.visible:
      children = copy.copy(v)
      children.parent = node
      children = visibility.expand_vert(problem, children)
      if children not in path:
        path.append(children)
        result, bottom_reached_search = ids_search(children, target,
                                                   current_depth + 1, max_depth,
                                                   path)
        if result is not None:
          return result, True
        bottom_reached = bottom_reached and bottom_reached_search

    return None, bottom_reached

  depth = 1
  i = 0
  bottom_reached = False
  root = problem["start_end_vertices"][0]
  root = visibility.expand_vert(problem, root)
  final_dest = problem["start_end_vertices"][1]
  while not bottom_reached:
    path = []
    path.append(root)
    result, bottom_reached = ids_search(root, final_dest, 0, depth, path)

    print(f'PATH: {i}')
    for p in path:
      print(p.name, end='-')
    print(f'\t New_limit:{depth}\n\n')

    print('BEST', end = ': ')
    a = copy.copy(path[-1])
    
    while a != None:
      print(a.name, end = '-')
      a = a.parent
    print('\n\n')

    problem["paths"].append([])
    problem["paths"][i].append(path)
    if result is not None:
      return path
    depth += 1
    i += 1
  return None


# Algoritmo A* Search
def a_star(problem):

  def heuristic_1(children, final_dest):
    return visibility.line_length(classes.LineSeg(children, final_dest))

  i = 0
  path = []

  open_list = []
  closed_list = []

  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  root = visibility.expand_vert(problem, root)
  open_list.append(root)

  while len(open_list) > 0:
    current = open_list.pop(0)
    closed_list.append(current)

    if current == final_dest:
      path = []
      while current != root:
        path.append(current)
        current = current.parent
      path.append(root)
      return path

    a = copy.copy(current)
    problem["paths"].append([])
    while a != None:
      problem["paths"][i].append(a)
      a = a.parent
    i += 1

    for v in current.visible:
      children = copy.copy(v)
      children.parent = current
      children = visibility.expand_vert(problem, children)

      if children in closed_list:
        continue

      dist_to_children = visibility.line_length(
          classes.LineSeg(current, children))
      children.distance = current.distance + dist_to_children + heuristic_1(
          children, final_dest)

      if children not in closed_list:
        open_list.append(children)

    open_list.sort(key=lambda v: v.distance)
  return path


# Algoritmo Iterative Deepening A*
def ida_star(problem):

  def search(current, final_dest, previous_cost, threshold, path):

    if current == final_dest:
      return True

    cost = previous_cost + visibility.line_length(
        classes.LineSeg(current, final_dest))

    if cost > threshold:
      return cost

    minimum = float('inf')
    for v in current.visible:
      children = copy.copy(v)
      children.parent = current

      children = visibility.expand_vert(problem, children)
      if children not in path:
        path.append(children)
        temp_cost = search(children, final_dest, cost, threshold, path)

        if temp_cost == True:
          return True

        if temp_cost < minimum:
          minimum = temp_cost

    return minimum

  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  root = visibility.expand_vert(problem, root)
  threshold = visibility.line_length(classes.LineSeg(root, final_dest))
  counter = 0

  while True:
    path = []
    path.append(root)

    temp_cost = search(root, final_dest, 0, threshold, path)

    print(f'PATH: {counter}')
    for p in path:
      print(p.name, end='-')
    print(f'\t New_limit:{temp_cost}\n\n')


    print('BEST', end = ': ')
    a = copy.copy(path[-1])
    while a != None:
      print(a.name, end = '-')
      a = a.parent
    print('\n\n')

    if temp_cost == True:
      return #RETORNAR O PATH AQUI (O MELHOR PATH A PARTIR DO PRINT DO a)
    elif temp_cost == float('inf'):
      return #NAO ACHOU SOLUCAÇÃO, RETORNA FALSE OU OUTRO PADRÃO
    else:
      threshold = temp_cost
      counter += 1
