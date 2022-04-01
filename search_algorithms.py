# Este módulo python contém implementações dos algoritmos de
# busca Best-First Search, Iterative Deepening Search, A*,
# e Iterative Deepening A*, aplicados ao problema de busca
# por um caminho de um ponto a outro do plano passando somente
# por vértices de polígonos sem que o caminho cruze qualquer
# aresta dos polígonos.

import copy

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
      return path[::-1]

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

    problem["paths"].append([])
    for p in path:
      problem["paths"][i].append(p)

    best_path = []
    a = copy.copy(path[-1])

    while a != None:
      best_path.append(a)
      a = a.parent

    if result is not None:
      return best_path[::-1]
    depth += 1
    i += 1
  return None


# Algoritmo A* Search
def a_star(problem):

  def heuristic_1(children, final_dest):
    return visibility.line_length(classes.LineSeg(children, final_dest))

  i = 0
  path = []

  # Inicializa vetores de controle
  open_list = []
  closed_list = []

  # Inicializa vértice inicial e final
  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  # Gera os filhos do vértice raiz
  root = visibility.expand_vert(problem, root)
  open_list.append(root)

  while len(open_list) > 0:
    
    # Retira o vértice com o menor f(x) = g(x) + h(x) e adiciona nos visitados
    current = open_list.pop(0)
    closed_list.append(current)

    # Caso o vértice atual é o final, encerra o programa retornando o caminho encontrado
    if current == final_dest:
      path = []
      while current != root:
        path.append(current)
        current = current.parent
      path.append(root)
      return path[::-1]

    a = copy.copy(current)
    problem["paths"].append([])
    while a != None:
      problem["paths"][i].append(a)
      a = a.parent
    i += 1

    # Para cada filho gerado, calcula o f(x) e adiciona na fila de prioridade
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

    # Ordena a fila baseado no f(x)
    open_list.sort(key=lambda v: v.distance)
  return path


# Algoritmo Iterative Deepening A*
def ida_star(problem):

  def search(current, final_dest, previous_cost, threshold, path):

    # Caso o vértice atual for o final, para o programa
    if current == final_dest:
      return True

    # Calcula o f(x) do nodo atual
    cost = previous_cost + visibility.line_length(
        classes.LineSeg(current, final_dest))

    # Caso o f(x) atual for maior que o f(x) máximo, retorna o f(x) atual
    if cost > threshold:
      return cost

    minimum = float('inf')

    # Para cada filho gerado, expande os nós e realiza a busca por profundidade baseado no f(x)
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

  # Inicializa os vértices inicial e final
  root = problem["start_end_vertices"][0]
  final_dest = problem["start_end_vertices"][1]

  # Gera os filhos da raíz
  root = visibility.expand_vert(problem, root)

  # Define o threshold inicial (distancia euclidiana entre o ponto inicial e final)
  threshold = visibility.line_length(classes.LineSeg(root, final_dest))
  counter = 0

  while True:
    path = []
    path.append(root)

    # Busca em profundidade, limitada pelo threshold
    temp_cost = search(root, final_dest, 0, threshold, path)

    problem["paths"].append([])
    for p in path:
      problem["paths"][counter].append(p)

    best_path = []
    a = copy.copy(path[-1])
    while a != None:
      best_path.append(a)
      a = a.parent

    if temp_cost == True:
      return best_path[::-1]
    elif temp_cost == float('inf'):
      return None
    else:
      threshold = temp_cost
      counter += 1
