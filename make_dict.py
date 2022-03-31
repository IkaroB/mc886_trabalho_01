# Exercício 1 de MO416A/MC886B 1s2022

# Este programa faz um dicionário com vértices, polígonos, e
# pontos de chegada e de partida a partir de um arquivo texto.

import classes


def make_dict(filepath):

  dict_data = {
      "vertices": [],
      "polygons": [],
      "start_end_vertices": [],
      "paths": []
  }

  with open(filepath, "r") as raw_data:

    start = False
    line = raw_data.readline()
    while (line):
      line = line.split()
      # Vertices
      if (len(line) == 3):
        new_vert = classes.Vertex(name=line[0], x=line[1], y=line[2])
        dict_data["vertices"].append(new_vert)

      # Polygons
      elif (len(line) > 3):
        poly_name = line[0]
        vert_names_list = line[1:]
        poly_vert_list = []
        for vert_name in vert_names_list:
          for vert in dict_data["vertices"]:
            if (vert_name == vert.name):
              poly_vert_list.append(vert)
              continue
        new_poly = classes.Polygon(poly_name, poly_vert_list)
        for vert in poly_vert_list:
          vert.belongs_poly = new_poly
        dict_data["polygons"].append(new_poly)

      # Start and end points
      elif (len(line) == 2):
        if not start:
          new_vert = classes.Vertex("S", line[0], line[1])
          start = True
        else:
          new_vert = classes.Vertex("G", line[0], line[1])
        dict_data["start_end_vertices"].append(new_vert)

      line = raw_data.readline()

  return dict_data
