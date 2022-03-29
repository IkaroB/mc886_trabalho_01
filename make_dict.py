# Exercício 1 de MO416A/MC886B 1s2022

# Este programa faz um dicionário com vértices, polígonos, e
# pontos de chegada e de partida a partir de um arquivo texto.

import classes


def make_dict():

  dict_data = {
      "vertices": [],
      "polygons": [],
      "start_end_vertices": [],
      "explored": []
  }

  with open("ex1-dados.txt", "r") as raw_data:

    start = False
    line = raw_data.readline()
    while (line):
      line = line.split()

      # Vertices
      if (len(line) == 3):
        new_vert = classes.Vertex(*line)
        #new_vert.print()
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
        new_poly = classes.Polygon(poly_name, *poly_vert_list)
        for vert in poly_vert_list:
          vert.belongs_to(new_poly)
        #new_poly.print()
        dict_data["polygons"].append(new_poly)

      # Start and end points
      elif (len(line) == 2):
        if not start:
          new_vert = classes.Vertex("S", *line)
          start = True
        else:
          new_vert = classes.Vertex("G", *line)
        #new_vert.print()
        dict_data["start_end_vertices"].append(new_vert)

      line = raw_data.readline()

  return dict_data


def main():
  return make_dict()


if __name__ == "__main__":
  main()
