# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém os algoritmos necessários para
# a expansão dos vértices, que consiste em descobrir quais
# outros vértices são visíveis para o vértice atual.

import numpy as np

import classes


# Registra no vértice atual (curr_vert) todos os outros
# vértices visíveis a partir dele.
def expand_vert(problem, curr_vert):

  visible = []
  curr_vert.visited = True

  for polygon in problem["polygons"]:

    # Checa o caso em que o polígono contém curr_vert.
    if (curr_vert.belongs_poly == polygon):
      visible_in_poly = get_visible_in_poly(curr_vert)
      for vis_vert in visible_in_poly:
        if (not vis_vert.visited):
          # print(vis_vert.name, "added from within the polygon")
          visible.append(vis_vert)

    # Outros polígonos.
    else:
      for i in range(len(polygon.vertices) - 1):
        poly_vert = polygon.vertices[i]
        possible_line = classes.LineSeg(curr_vert, poly_vert)
        if (is_visible(possible_line, problem)):
          if (not poly_vert.visited):
            # print(poly_vert.name, "added from another polygon")
            visible.append(poly_vert)

  # Checa o caso em que o destino é visível
  goal = problem["start_end_vertices"][1]
  possible_line = classes.LineSeg(curr_vert, goal)
  if (is_visible(possible_line, problem)):
    if (not goal.visited):
      visible.append(goal)

  curr_vert.visible = visible
  return curr_vert


# Retorna True se o segmento de reta não cruza nenhum polígono
# e False se há cruzamento.
def is_visible(possible_line, problem):

  for polygon in problem["polygons"]:
    #print(polygon)
    if (do_cross_poly(possible_line, polygon)):
      return False

  return True


# Checa a concavidade dos polígonos e altera os atributos "bay"
# e "concavity" nos polígonos que possuem concavidade.
def make_concavity(problem):

  for polygon in problem["polygons"]:
    polygon = poly_concavity(polygon)

  return problem


# Como, na definição do problema, os vértices foram declarados
# no sentido anti-horário, quando a orientação de 3 pontos
# consecutivos for no sentido horário, eles fazem parte da baía.
# A função constrói o vetor "bay" e define o valor do parâmetro
# "concavity" como True no polígono de entrada, se ele possuir
# alguma concavidade.
def poly_concavity(polygon):

  no_vert = len(polygon.vertices) - 1
  if (no_vert > 3):
    for i in range(no_vert):
      v1 = polygon.vertices[i]
      v2 = polygon.vertices[(i + 1) % no_vert]
      v3 = polygon.vertices[(i + 2) % no_vert]
      p1 = v1.coord
      p2 = v2.coord
      p3 = v3.coord

      #print(f"\nPolygon: {polygon.name}, vertices: {v1.name}, {v2.name}, {v3.name};")
      #print("\tx:" + p1.x,p2.x,p3.x)
      #print("\ty:" + p1.y,p2.y,p3.y)

      # Constrói a baía e modifica o parâmetro de
      # concavidade.
      if (orientation(p1, p2, p3) == -1):
        polygon.concavity = True
        for bay_vert in [v1, v2, v3]:
          if (bay_vert not in polygon.bay):
            polygon.bay.append(bay_vert)

  return polygon


# Calcula se os três pontos ordenados são orientados no sentido
# horário (negativo), anti-horário (positivo) ou são colineares
# (zero).
def orientation(p1, p2, p3):

  m = [[float(p1.x), float(p2.x), float(p3.x)],
       [float(p1.y), float(p2.y), float(p3.y)], [1.0, 1.0, 1.0]]
  det = np.linalg.det(m)
  #print("\tdet:", det)

  # O determinante do numpy nem sempre retorna zero quando
  # há colinearidade.
  if (abs(det) < 0.000001):
    orientation = 0
  elif (det < 0):
    orientation = -1
  elif (det > 0):
    orientation = 1

  #print("\torientation:", orientation)

  return orientation


# Retorna todos os vértices visíveis para "vert" que estão
# no mesmo polígono que ele.
def get_visible_in_poly(vert):

  visible = []
  polygon = vert.belongs_poly

  # Checa se o polígono que contém "vert" tem concavidade.
  # Se "vert" estiver na baía, todos pertencentes a ela são
  # visíveis, bem como seus adjacentes, e ainda, os
  # vértices adjacentes a seus visíveis, caso sejam
  # colineares à reta que os une.
  # Caso contrário, somente os adjacentes a "vert".
  if (polygon.concavity and vert in polygon.bay):
    visible = []
    for v in polygon.bay:
      visible.append(v)
    visible.remove(vert)

    for adj in get_adjacent(vert):
      if adj not in visible:
        visible.append(adj)

    for vis_vert in visible:
      for other_vis in get_adjacent(vis_vert):
        p1 = vert.coord
        p2 = vis_vert.coord
        p3 = other_vis.coord
        if (other_vis not in visible and other_vis != vert):
          if (orientation(p1, p2, p3) == 0):
            visible.append(other_vis)

  else:
    visible = get_adjacent(vert)

  return visible


def get_adjacent(vert):

  adjacent = vert.adjacent

  if not adjacent:
    polygon = vert.belongs_poly
    if vert.belongs_poly:
      no_vert = len(polygon.vertices) - 1
      for i in range(no_vert):
        if (vert == polygon.vertices[i]):
          index_1 = (i - 1) % no_vert
          index_2 = (i + 1) % no_vert
          adjacent.append(polygon.vertices[index_1])
          adjacent.append(polygon.vertices[index_2])
          #print("Adjacent:", polygon.vertices[index_1].name,
          #polygon.vertices[index_2].name)
          break

  return adjacent


def is_adjacent(v1, v2):
  if v1 in get_adjacent(v2):
    return True
  else:
    return False


# Entrada: dois segmentos de reta, que são formados por dois
# vértices cada.
# A função retorna True se os segmentos se cruzam, e False
# caso contrário.
# Se os segmentos se cruzam em um ponto apenas, considera-se
# que não se cruzam, já que os vértices se enxergam.
# Nos casos de colinearidade, também considera-se que não
# se cruzam, pelo mesmo motivo.
def do_cross_seg(line_seg_1, line_seg_2):

  p1 = line_seg_1.v1.coord
  p2 = line_seg_1.v2.coord

  p3 = line_seg_2.v1.coord
  orientation_1 = orientation(p1, p2, p3)

  p3 = line_seg_2.v2.coord
  orientation_2 = orientation(p1, p2, p3)

  if (orientation_1 == 0 and orientation_2 == 0):
    #print(f"{line_seg_1.v1.name}-{line_seg_1.v2.name}: ", end="")
    #print(line_seg_2.v1.name, line_seg_2.v2.name)
    return [line_seg_2.v1, line_seg_2.v2]

  if (orientation_1 == 0):
    return line_seg_2.v1

  if (orientation_2 == 0):
    return line_seg_2.v2

  if (orientation_1 == orientation_2):
    return "No"

  else:
    return "Yes"


# Checa se um segmento de reta cruza alguma das arestas
# de um polígono.
def do_cross_poly(line_seg, polygon):

  collinear = []

  for i in range(len(polygon.vertices) - 1):
    v1 = polygon.vertices[i]
    v2 = polygon.vertices[i + 1]

    if (line_seg.v1 in (v1, v2)):
      continue
    elif (line_seg.v2 in (v1, v2)):
      continue

    edge = classes.LineSeg(v1, v2)

    cross_seg_1 = do_cross_seg(line_seg, edge)
    cross_seg_2 = do_cross_seg(edge, line_seg)

    if (cross_seg_1 == cross_seg_2) and (cross_seg_1 == "Yes"):
      return True
    elif (cross_seg_1 == "No" or cross_seg_2 == "No"):
      continue
    elif (type(cross_seg_1) is list):
      for coll_vert in cross_seg_1:
        collinear.append(coll_vert)

    # Pelo menos um dos vértices da aresta em questão
    # está contido no segmento de reta.
    else:
      # Se for adjacente ao vértice de destino (que está
      # em um polígono diferente do vértice de partida),
      # então o vértice em cross_seg_1 é visível.
      # Se for adjacente ao vértice de partida, também.
      not_added = cross_seg_1 not in collinear
      start_adjacent = get_adjacent(line_seg.v1)
      dest_adjacent = get_adjacent(line_seg.v2)
      if (cross_seg_1 in dest_adjacent or cross_seg_1 in start_adjacent):
        continue
      elif (not_added):
        collinear.append(cross_seg_1)

    # if collinear:
    #   print(f"Collinear to {line_seg.v1.name}-{line_seg.v2.name}: ", end="")
    #   for aux_vert in collinear:
    #     print(aux_vert.name, end=" ")
    #   print("\n")

  # Um dicionário contendo como chaves cada um dos
  # polígonos que contêm os vértices colineares ao
  # segmento de reta atual, cujos valores são arrays
  # contendo seus respectivos vértices que pertencem
  # ao array "collinear".
  aux_dic = {}

  for vert in collinear:

    polygon = vert.belongs_poly
    if not aux_dic.keys():
      aux_dic[polygon.name] = [vert]

    elif polygon.name not in aux_dic.keys():
      aux_dic[polygon.name] = [vert]

    else:
      aux_dic[polygon.name].append(vert)

  for poly_name in aux_dic.keys():
    for vert in aux_dic[poly_name]:

      # Este loop deve contemplar os casos nos quais
      # há vários vértices colineares ao segmento
      # atual em um certo polígono. Caso algum
      # desses vértices não for adjacente a nenhum
      # dos outros, e ele não estiver em uma baía,
      # então há cruzamento.
      do_continue = False
      for aux_v in get_adjacent(vert):
        if aux_v in aux_dic[poly_name]:
          do_continue = True

      if do_continue:
        continue

      # Se o comprimento de line_seg for maior que a
      # distância de seus dois vértices a algum dos
      # vértices colineares selecionados, então o
      # segmento cruza algum polígono.
      aux_seg_1 = classes.LineSeg(line_seg.v1, vert)
      aux_seg_2 = classes.LineSeg(line_seg.v2, vert)
      seg_length = line_length(line_seg)
      comp_1 = seg_length > line_length(aux_seg_1)
      comp_2 = seg_length > line_length(aux_seg_2)
      if (comp_1 and comp_2):
        return True

  return False


# Retorna o tamanho de um segmento de reta.
def line_length(line_seg):

  x_diff = line_seg.v1.coord.x - line_seg.v2.coord.x
  y_diff = line_seg.v1.coord.y - line_seg.v2.coord.y

  length = (x_diff**2 + y_diff**2)**0.5

  return length


# Printa todos os vértices visíveis a partir de "vert"
def vert_visibility(vert):

  if vert.visible:
    print(f"Vertex {vert.name} sees: ", end="")
    for vert in vert.visible:
      print(f"{vert.name}", end=" ")
  else:
    print(f"Vertex {vert.name} not expanded.", end="")
  print("\n")


# Revela todas as concavidades do problema.
def print_bays(problem):

  for polygon in problem["polygons"]:
    if polygon.concavity:
      print(f"\nPolygon {polygon.name} has a bay.")
      print("Bay:", end="")
      for vert in polygon.bay:
        print(vert.name, end=" ")
      print("\n")

  return


def debug_vert_visibility(problem, vert):
  expand_vert(problem, vert)
  vert_visibility(vert)


# def expand_all(problem, node):
#   if node == problem["start_end_vertices"][1]:
#     return (problem, node)
#   else:
#     node = expand_vert(problem, node)
#     for v in node.visible:
#       expand_all(problem, v)
