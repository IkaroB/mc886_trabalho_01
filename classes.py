# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém as classes usadas no exercício.

import visibility


class LineSeg:

  def set_weight(self):
    self.weight = visibility.line_length(self)

  def __init__(self, v1, v2):
    self.v1 = v1
    self.v2 = v2

  def __eq__(self, other):
    return (self.v1 == other.v1) and (self.v2 == other.v2)

  def __lt__(self, other):
    return self.weight < other.weight


class Vertex:

  def __init__(self, name, x, y):
    self.name = name
    self.coord = Point(x, y)
    self.visible = []
    self.belongs_poly = None
    self.adjacent = []
    self.distance = 0
    self.visited = False
    self.parent = None

  def __eq__(self, other):
    if other.__class__ == Point:
      return self.coord.x == other.x and self.coord.y == other.y
    elif other.__class__ == Vertex:
      return self.name == other.name
    else:
      return False

  def __lt__(self, other):
    return self.distance < other.distance

  def print(self):
    out = f"{self.name}: x={self.coord.x}, y={self.coord.y};"
    if self.visible:
      out += f"\tVisible:{self.visible}"
    if self.belongs_poly:
      out += f"\tBelongs to:{self.belongs_poly.name}\n"
    return out

  def __str__(self):
    out = f"{self.name}: x={self.coord.x}, y={self.coord.y};"
    if self.visible:
      out += f"\tVisible: "
      for v in self.visible:
        out += f"{v.name} "
    if self.belongs_poly:
      out += f"\tBelongs to:{self.belongs_poly.name}\n"
    return out

  def belongs_to(self, polygon):
    self.belongs_poly = polygon

  def set_visited(self, value):
    self.visited = value

  def get_visited(self):
    return self.visited

  def set_distance_and_visited(self, dest):
    self.visited = True
    self.distance = visibility.line_length(LineSeg(self, dest))


class Polygon:

  def __init__(self, name, vertices):
    self.name = name
    self.vertices = vertices
    self.concavity = False
    self.bay = []

  def __str__(self):
    out = f"{self.name}:"
    if self.vertices:
      for vert in self.vertices:
        out += "\t"
        out += str(vert)
    else:
      out += "Sem vertices definidos"
    out += "\n"
    return out


class Point:

  def __init__(self, x, y):
    self.x = float(x)
    self.y = float(y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def print(self):
    print(f"x={self.x}, y={self.y};")
